import streamlit as st
import ccxt
import pandas as pd
import requests

# --- CONFIGURACIÓN ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

# Configuración básica
st.set_page_config(page_title="OMEGA PRO", layout="centered")

def send_telegram_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url, timeout=5)
    except Exception as e:
        st.error(f"Error enviando mensaje: {e}")

st.title("OMEGA PRO: Panel de Control")

try:
    exchange = ccxt.binance({'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=50)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    precio_actual = df['close'].iloc[-1]
    
    st.success(f"Conexión exitosa. Precio actual: {precio_actual}")
    
    if st.button("Enviar Alerta de Prueba"):
        send_telegram_msg(f"Prueba de Omega Pro. Precio BTC: {precio_actual}")
        st.write("Alerta enviada.")

except Exception as e:
    st.error(f"Error conectando con el mercado: {e}")
