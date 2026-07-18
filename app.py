import streamlit as st
import yfinance as yf
import requests

# --- CONFIGURACIÓN ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

st.set_page_config(page_title="OMEGA PRO", layout="centered")

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)

st.title("OMEGA PRO: Panel de Control")

try:
    # Usamos Yahoo Finance para evitar bloqueos
    ticker = yf.Ticker("BTC-USD")
    data = ticker.history(period="1d", interval="1h")
    precio_actual = data['Close'].iloc[-1]
    
    st.success(f"Conexión estable. Precio actual BTC: ${precio_actual:.2f}")
    
    if st.button("Enviar Alerta de Prueba"):
        send_telegram_msg(f"Omega Pro activo. Precio BTC: ${precio_actual:.2f}")
        st.write("Alerta enviada correctamente.")

except Exception as e:
    st.error(f"Error conectando con el mercado: {e}")
