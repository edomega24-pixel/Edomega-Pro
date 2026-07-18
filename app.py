import streamlit as st
import yfinance as yf
import requests
import os

# --- Configuración ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"

# --- JavaScript para Auto-Refresh ---
# Esto le dice al navegador que recargue la página cada 30 segundos
st.markdown("""
    <meta http-equiv="refresh" content="30">
""", unsafe_allow_html=True)

# --- Funciones de Gestión ---
@st.cache_data(ttl=20)
def get_market_data():
    ticker = yf.Ticker("BTC-USD")
    return ticker.history(period="1d", interval="1m")

def get_saved_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read()
    return "ESPERA_NEUTRAL"

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.set_page_config(page_title="OMEGA PRO", layout="wide")
st.title("🚀 OMEGA PRO: Monitoreo Autónomo")

# --- Obtención de Datos ---
df = get_market_data()
last_close = df['Close'].iloc[-1]
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

# --- Lógica de Motores ---
status_ema = "ALCISTA" if last_close > (ema200 * 1.001) else "BAJISTA" if last_close < (ema200 * 0.999) else "ESPERA"
status_bos = "COMPRA" if last_close > high_prev else "VENTA" if last_close < low_prev else "NEUTRAL"

# --- Interfaz Visual ---
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

# --- Notificación y Sinergia ---
current_total_status = f"{status_bos}_{status_ema}"
last_saved = get_saved_status()

if (status_bos == "COMPRA" and status_ema == "ALCISTA") or (status_bos == "VENTA" and status_ema == "BAJISTA"):
    st.markdown("""<div style="background-color: purple; color: white; padding: 20px; border-radius: 10px; text-align: center;">🔥 SINERGIA TOTAL ALINEADA 🔥</div>""", unsafe_allow_html=True)

if current_total_status != last_saved:
    send_telegram_msg(f"🚀 OMEGA PRO:\nBOS: {status_bos}\nEMA 200: {status_ema}")
    save_status(current_total_status)

st.divider()
st.write(f"**Precio Actual:** {last_close:.2f} | **EMA 200:** {ema200:.2f}")
st.caption("El sistema se actualiza automáticamente cada 30 segundos. ¡No necesitas hacer nada!")
