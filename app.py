import streamlit as st
import yfinance as yf
import requests
import datetime

TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

# Inicializar estados
if 'historial' not in st.session_state:
    st.session_state.historial = []
if 'last_status' not in st.session_state:
    st.session_state.last_status = "NEUTRAL"

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

def agregar_al_historial(tipo):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.historial.append({"Fecha": timestamp, "Señal": tipo})
    if len(st.session_state.historial) > 24:
        st.session_state.historial.pop(0)

st.title("OMEGA PRO: Panel de Control")

# --- INDICADOR DE ESTADO ACTUAL ---
st.subheader("Estado Operativo Actual")
if st.session_state.last_status == "COMPRA":
    st.success(f"EL SISTEMA ESTÁ EN MODO: {st.session_state.last_status}")
elif st.session_state.last_status == "VENTA":
    st.error(f"EL SISTEMA ESTÁ EN MODO: {st.session_state.last_status}")
else:
    st.info(f"EL SISTEMA ESTÁ EN MODO: {st.session_state.last_status}")

ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="5d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

st.write(f"Precio Actual BTC: {last_close:.2f}")

# Lógica de estados
if last_close > high_prev and st.session_state.last_status != "COMPRA":
    st.session_state.last_status = "COMPRA"
    msg = "🚀 OMEGA PRO: BOS Alcista detectado. Sugerencia: Buscar COMPRAS."
    send_telegram_msg(msg)
    agregar_al_historial("COMPRA")

elif last_close < low_prev and st.session_state.last_status != "VENTA":
    st.session_state.last_status = "VENTA"
    msg = "📉 OMEGA PRO: BOS Bajista detectado. Sugerencia: Buscar VENTAS."
    send_telegram_msg(msg)
    agregar_al_historial("VENTA")

elif low_prev <= last_close <= high_prev and st.session_state.last_status != "NEUTRAL":
    st.session_state.last_status = "NEUTRAL"
    msg = "⚠️ OMEGA PRO: Mercado en zona neutral."
    send_telegram_msg(msg)
    agregar_al_historial("NEUTRAL")

# Mostrar Historial
st.subheader("Historial de Señales (Últimas 24)")
if st.session_state.historial:
    st.table(st.session_state.historial)
