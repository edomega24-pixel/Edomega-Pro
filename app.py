import streamlit as st
import yfinance as yf
import requests
import os
import pandas as pd
import base64

# --- Configuración ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"
HISTORY_FILE = "history.csv"
LOG_FILE = "log_sinergias.csv"

# --- Funciones de Alerta ---
def reproducir_alerta(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'''<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'''
            st.markdown(audio_html, unsafe_allow_html=True)

# --- Funciones de Datos (Optimizadas contra bloqueo) ---
def get_trend_5m():
    try:
        df = yf.Ticker("BTC-USD").history(period="1d", interval="5m")
        if df.empty: return "NEUTRAL"
        ema200_5m = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
        last_close_5m = df['Close'].iloc[-1]
        return "ALCISTA" if last_close_5m > ema200_5m else "BAJISTA"
    except: return "NEUTRAL"

def get_market_data():
    try:
        # Descarga sin caché estricta para forzar datos en tiempo real y evitar congelamiento
        ticker = yf.Ticker("BTC-USD")
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None
        return df
    except Exception as e:
        return None

def calcular_atr(df, period=14):
    high = df['High']
    low = df['Low']
    close = df['Close'].shift(1)
    
    tr1 = high - low
    tr2 = (high - close).abs()
    tr3 = (low - close).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean().iloc[-1]
    return atr

def registrar_sinergia(precio, tendencia, vol, vol_avg, atr):
    data = {
        'Timestamp': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")],
        'Precio': [precio],
        'Tendencia_5m': [tendencia],
        'Volumen_Actual': [vol],
        'Vol_Promedio': [vol_avg],
        'ATR': [atr]
    }
    df_log = pd.DataFrame(data)
    if not os.path.exists(LOG_FILE):
        df_log.to_csv(LOG_FILE, index=False)
    else:
        df_log.to_csv(LOG_FILE, mode='a', header=False, index=False)

def update_history(bos, ema):
    new_entry = pd.DataFrame({'BOS': [bos], 'EMA': [ema]})
    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
        history = pd.concat([history, new_entry]).tail(10)
    else:
        history = new_entry
    history.to_csv(HISTORY_FILE, index=False)
    return history

# --- Interfaz ---
st.set_page_config(page_title="OMEGA PRO", layout="wide")
st.title("🚀 OMEGA PRO: Panel Maestro Multitemporal + ATR")

# --- Auto-Refresh ---
st.markdown('<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)

df = get_market_data()
trend_5m = get_trend_5m()

if df is not None and not df.empty:
    last_close = df['Close'].iloc[-1]
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    if len(df) >= 26:
        high_prev = df['High'].iloc[-26:-1].max()
        low_prev = df['Low'].iloc[-26:-1].min()
    else:
        high_prev = df['High'].max()
        low_prev = df['Low'].min()

    vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else df['Volume'].mean()
    last_vol = df['Volume'].iloc[-1]
    
    atr_val = calcular_atr(df, period=min(14, len(df))) if len(df) > 1 else 0.0
    atr_medio = last_close * 0.0005 

    status_ema = "ALCISTA" if last_close > (ema200 * 1.001) else "BAJISTA" if last_close < (ema200 * 0.999) else "ESPERA"
    status_bos = "COMPRA" if last_close > high_prev else "VENTA" if last_close < low_prev else "NEUTRAL"

    # --- Visualización con Colores en los 3 paneles independientes ---
    col1, col2, col3 = st.columns(3)
    if status_bos == "COMPRA": col1.success(f"Motor BOS: {status_bos}")
    elif status_bos == "VENTA": col1.error(f"Motor BOS: {status_bos}")
    else: col1.warning(f"Motor BOS: {status_bos}")

    if status_ema == "ALCISTA": col2.success(f"Motor EMA 200: {status_ema}")
    elif status_ema == "BAJISTA": col2.error(f"Motor EMA 200: {status_ema}")
    else: col2.warning(f"Motor EMA 200: {status_ema}")
    
    col3.info(f"Tendencia 5m: {trend_5m}")

    # --- Historial ---
    st.subheader("📜 Historial de Movimientos")
    historial = update_history(status_bos, status_ema)
    st.table(historial)

    # --- Notificación y Sinergia ---
    es_sinergia = (status_bos == "COMPRA" and status_ema == "ALCISTA" and trend_5m == "ALCISTA") or \
                  (status_bos == "VENTA" and status_ema == "BAJISTA" and trend_5m == "BAJISTA")
    
    if es_sinergia and last_vol > vol_avg and atr_val > atr_medio:
        st.markdown(
            """
            <div style="background-color: #6a0dad; padding: 15px; border-radius: 10px; text-align: center;">
                <h2 style="color: white; margin: 0;">💎 SINERGIA PRO: ¡CONFIRMADA! (BOS + EMA + 5m + ATR)</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        registrar_sinergia(last_close, trend_5m, last_vol, vol_avg, atr_val)
        reproducir_alerta('alerta_especial.mp3.mp3')
    elif status_bos != "NEUTRAL":
        reproducir_alerta('campana.mp3.mp3')

    # --- Telegram ---
    current_status = f"{status_bos}_{status_ema}_{trend_5m}"
    if not os.path.exists(STATUS_FILE) or open(STATUS_FILE).read() != current_status:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Omega Pro Update: {current_status}")
        with open(STATUS_FILE, "w") as f: f.write(current_status)

    st.write(f"Precio en vivo: {last_close:.2f} | EMA 200: {ema200:.2f} | Volumen: {last_vol:.0f} (Promedio: {vol_avg:.0f}) | ATR: {atr_val:.2f}")
else:
    st.error("⚠️ Conexión con Yahoo Finance pausada temporalmente. Reintentando reconexión en el próximo ciclo...")
