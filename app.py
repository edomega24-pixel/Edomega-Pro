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

# Usamos el archivo como fuente de verdad
current_status = get_saved_status()

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.title("OMEGA PRO: Panel de Control (Sync)")

# Indicador de estado basado en archivo
st.subheader(f"Estado Operativo: {current_status}")

ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="5d", interval="1h")
last_close = df['Close'].iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

# Lógica de cambio
if last_close > high_prev and current_status != "COMPRA":
    save_status("COMPRA")
    send_telegram_msg("🚀 OMEGA PRO: BOS Alcista detectado. Sugerencia: Buscar COMPRAS.")
elif last_close < low_prev and current_status != "VENTA":
    save_status("VENTA")
    send_telegram_msg("📉 OMEGA PRO: BOS Bajista detectado. Sugerencia: Buscar VENTAS.")
elif low_prev <= last_close <= high_prev and current_status != "NEUTRAL":
    save_status("NEUTRAL")
    send_telegram_msg("⚠️ OMEGA PRO: Mercado en zona neutral.")

st.write(f"Precio Actual BTC: {last_close:.2f}")
