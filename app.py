import streamlit as st
import yfinance as yf
import requests
import os

# --- Configuración ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"

def get_saved_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read()
    return "ESPERA"

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.title("OMEGA PRO: Panel Maestro Unificado")

# --- Datos ---
ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="10d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]

# --- Lógica de Motores ---
# 1. Motor EMA 200 (Estricto)
cruce_alcista = last_close > (ema200 * 1.001)
cruce_bajista = last_close < (ema200 * 0.999)
status_ema = "ALCISTA" if cruce_alcista else "BAJISTA" if cruce_bajista else "ESPERA"

# 2. Motor BOS (Dinámico)
status_bos = "COMPRA" if last_close > high_prev else "VENTA" if last_close < low_prev else "NEUTRAL"

# --- Visualización (Semáforos) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Motor BOS")
    if status_bos == "COMPRA": st.success("COMPRA")
    elif status_bos == "VENTA": st.error("VENTA")
    else: st.warning("NEUTRAL")

with col2:
    st.subheader("Motor EMA 200")
    if status_ema == "ALCISTA": st.success("ALCISTA")
    elif status_ema == "BAJISTA": st.error("BAJISTA")
    else: st.warning("ESPERA")

# --- Estado del Sistema ---
st.divider()
st.write(f"**Precio Actual:** {last_close:.2f} | **EMA 200:** {ema200:.2f}")

# Notificación automática si el sistema cambia
current_total_status = f"{status_bos}_{status_ema}"
last_saved = get_saved_status()

if current_total_status != last_saved:
    send_telegram_msg(f"🚀 OMEGA PRO:\nBOS: {status_bos}\nEMA 200: {status_ema}")
    save_status(current_total_status)
