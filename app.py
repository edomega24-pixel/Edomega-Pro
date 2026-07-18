import streamlit as st
import yfinance as yf
import requests
import datetime
import os

TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"

def get_saved_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read()
    return "NEUTRAL"

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.title("OMEGA PRO: Panel Unificado (Dinámico + EMA 200)")

# Datos
ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="10d", interval="1h")
last_close = df['Close'].iloc[-1]
# Rango dinámico
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()
# EMA 200
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]

current_status = get_saved_status()

# Lógica Unificada
st.subheader(f"Estado Operativo: {current_status}")
st.write(f"Precio: {last_close:.2f} | EMA 200: {ema200:.2f}")

# 1. Filtro Dinámico (BOS)
bos_signal = None
if last_close > high_prev: bos_signal = "COMPRA (BOS Dinámico)"
elif last_close < low_prev: bos_signal = "VENTA (BOS Dinámico)"

# 2. Filtro Estructural (EMA 200)
ema_signal = "Alcista (Precio > EMA)" if last_close > ema200 else "Bajista (Precio < EMA)"

# Notificación inteligente
if bos_signal and bos_signal.split()[0] != current_status:
    new_status = bos_signal.split()[0]
    save_status(new_status)
    msg = f"🚀 OMEGA PRO:\nAcción: {bos_signal}\nFiltro Estructural: {ema_signal}"
    send_telegram_msg(msg)
    st.success(msg)

elif not bos_signal and current_status != "NEUTRAL":
    save_status("NEUTRAL")
    send_telegram_msg("⚠️ OMEGA PRO: Mercado en zona neutral (Sin BOS).")
