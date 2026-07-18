import streamlit as st
import yfinance as yf
import requests

TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.title("OMEGA PRO: Motor BOS Activo")

# Análisis de Estructura
ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="5d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

st.write(f"Precio Actual: {last_close:.2f}")
st.write(f"Rango de Estructura: {low_prev:.2f} - {high_prev:.2f}")

# Detección de BOS
if last_close > high_prev:
    msg = "🚀 OMEGA PRO: BOS Alcista detectado en BTC/USD"
    send_telegram_msg(msg)
    st.success(msg)
elif last_close < low_prev:
    msg = "📉 OMEGA PRO: BOS Bajista detectado en BTC/USD"
    send_telegram_msg(msg)
    st.error(msg)
else:
    st.info("El precio se mantiene dentro del rango de estructura.")
