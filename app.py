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

# --- Función de Alertas ---
def reproducir_alerta(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'''
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            '''
            st.markdown(audio_html, unsafe_allow_html=True)

# --- Auto-Refresh ---
st.markdown('<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)

# --- Funciones ---
@st.cache_data(ttl=20)
def get_market_data():
    try:
        ticker = yf.Ticker("BTC-USD")
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None
        return df
    except Exception as e:
        st.error("Error conectando con el mercado.")
        return None

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
st.title("🚀 OMEGA PRO: Panel Maestro")

df = get_market_data()

if df is not None:
    last_close = df['Close'].iloc[-1]
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    high_prev = df['High'].iloc[-26:-1].max()
    low_prev = df['Low'].iloc[-26:-1].min()
    
    # Filtro de Volumen
    vol_avg = df['Volume'].rolling(window=20).mean().iloc[-1]
    last_vol = df['Volume'].iloc[-1]

    status_ema = "ALCISTA" if last_close > (ema200 * 1.001) else "BAJISTA" if last_close < (ema200 * 0.999) else "ESPERA"
    status_bos = "COMPRA" if last_close > high_prev else "VENTA" if last_close < low_prev else "NEUTRAL"

    # --- Visualización con Colores ---
    col1, col2 = st.columns(2)
    if status_bos == "COMPRA": col1.success(f"Motor BOS: {status_bos}")
    elif status_bos == "VENTA": col1.error(f"Motor BOS: {status_bos}")
    else: col1.warning(f"Motor BOS: {status_bos}")

    if status_ema == "ALCISTA": col2.success(f"Motor EMA 200: {status_ema}")
    elif status_ema == "BAJISTA": col2.error(f"Motor EMA 200: {status_ema}")
    else: col2.warning(f"Motor EMA 200: {status_ema}")

    # --- Historial ---
    st.subheader("📜 Historial de Movimientos")
    historial = update_history(status_bos, status_ema)
    st.table(historial)

    # --- Notificación y Sinergia ---
    if (status_bos == "COMPRA" and status_ema == "ALCISTA") or (status_bos == "VENTA" and status_ema == "BAJISTA"):
        if last_vol > vol_avg:
            st.markdown("### 🔥 SINERGIA TOTAL CON VOLUMEN 🔥")
            reproducir_alerta('alerta_especial.mp3.mp3')
        else:
            st.warning("⚠️ Sinergia detectada pero bajo volumen")
            reproducir_alerta('campana.mp3.mp3')
    elif status_bos != "NEUTRAL":
        reproducir_alerta('campana.mp3.mp3')

    # --- Telegram ---
    current_status = f"{status_bos}_{status_ema}"
    if not os.path.exists(STATUS_FILE) or open(STATUS_FILE).read() != current_status:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Omega Pro: {current_status}")
        with open(STATUS_FILE, "w") as f: f.write(current_status)

    st.write(f"Precio Actual: {last_close:.2f} | EMA 200: {ema200:.2f} | Volumen: {last_vol:.0f} (Promedio: {vol_avg:.0f})")
else:
    st.warning("Esperando datos del mercado...")
