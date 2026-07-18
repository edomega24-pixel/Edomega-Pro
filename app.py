import streamlit as st
import ccxt
import pandas as pd
import requests

# --- CONFIGURACIÓN ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)

# Configuración de arquitectura
st.set_page_config(page_title="OMEGA PRO - ENGINE", layout="wide")
exchange = ccxt.binance({'enableRateLimit': True})

def fetch_data(symbol, timeframe='1h', limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

st.title("OMEGA PRO: Motor con Notificaciones")
data = fetch_data('BTC/USDT')
precio_actual = data['close'].iloc[-1]
st.write(f"Precio actual de BTC: {precio_actual}")

if st.button("Enviar Alerta de Prueba"):
    send_telegram_msg(f"Omega Pro: Prueba de sistema. Precio actual BTC: {precio_actual}")
    st.success("Mensaje enviado a Telegram")
