import streamlit as st
import yfinance as yf
import requests

TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

# Inicializamos el estado de la última alerta en la sesión de Streamlit
if 'last_status' not in st.session_state:
    st.session_state.last_status = "NEUTRAL"

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.title("OMEGA PRO: Motor de Análisis Estructural")

ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="5d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

st.write(f"Precio Actual: {last_close:.2f}")

# Lógica de estados
if last_close > high_prev and st.session_state.last_status != "COMPRA":
    msg = "🚀 OMEGA PRO: BOS Alcista detectado. Sugerencia: Buscar COMPRAS."
    send_telegram_msg(msg)
    st.session_state.last_status = "COMPRA"
    st.success(msg)

elif last_close < low_prev and st.session_state.last_status != "VENTA":
    msg = "📉 OMEGA PRO: BOS Bajista detectado. Sugerencia: Buscar VENTAS."
    send_telegram_msg(msg)
    st.session_state.last_status = "VENTA"
    st.error(msg)

elif low_prev <= last_close <= high_prev and st.session_state.last_status != "NEUTRAL":
    msg = "⚠️ OMEGA PRO: Mercado en zona neutral. No hay señales activas."
    send_telegram_msg(msg)
    st.session_state.last_status = "NEUTRAL"
    st.info(msg)

else:
    st.write(f"Estado actual: {st.session_state.last_status}. Monitoreando...")
