import streamlit as st
import yfinance as yf
import requests
import datetime
import os

TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"

# --- Funciones de Gestión ---
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

st.title("OMEGA PRO: Panel de Sinergia")

# --- Datos ---
ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="10d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]

# --- Lógica de Señales ---
# 1. Estado BOS
bos_status = "NEUTRAL"
if last_close > high_prev: bos_status = "COMPRA"
elif last_close < low_prev: bos_status = "VENTA"

# 2. Estado EMA 200
ema_status = "ALCISTA" if last_close > ema200 else "BAJISTA"

# --- Interfaz Visual (Semáforo) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("BOS Dinámico")
    if bos_status == "COMPRA": st.success("COMPRA (BOS)")
    elif bos_status == "VENTA": st.error("VENTA (BOS)")
    else: st.warning("NEUTRAL (BOS)")

with col2:
    st.subheader("Tendencia EMA 200")
    if ema_status == "ALCISTA": st.success("ALCISTA (EMA 200)")
    else: st.error("BAJISTA (EMA 200)")

# --- Lógica de Sinergia (Púrpura) ---
st.divider()
if (bos_status == "COMPRA" and ema_status == "ALCISTA") or (bos_status == "VENTA" and ema_status == "BAJISTA"):
    st.markdown("""
        <div style="background-color: purple; color: white; padding: 20px; border-radius: 10px; text-align: center; font-size: 20px;">
        🔥 SINERGIA TOTAL DETECTADA (BOS + EMA ALINEADOS) 🔥
        </div>
    """, unsafe_allow_html=True)
    
    # Notificación especial si hubo cambio
    last_saved = get_saved_status()
    if last_saved != "SINERGIA":
        send_telegram_msg("🟣 OMEGA PRO: ¡ALINEACIÓN TOTAL DETECTADA! EMA 200 y BOS coinciden.")
        save_status("SINERGIA")
else:
    # Si no hay sinergia, guardamos el estado normal
    save_status(bos_status)

st.write(f"Precio Actual: {last_close:.2f} | EMA 200: {ema200:.2f}")
