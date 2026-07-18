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

st.title("OMEGA PRO: Panel Maestro (Versión Unificada)")

# --- Datos ---
ticker = yf.Ticker("BTC-USD")
df = ticker.history(period="10d", interval="1h")
last_close = df['Close'].iloc[-1]
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]

# --- Lógica Estricta de EMA 200 (Como la tenías local) ---
# Usamos una tolerancia para evitar disparos falsos si el precio toca la EMA
cruce_alcista = last_close > (ema200 * 1.001) 
cruce_bajista = last_close < (ema200 * 0.999)

status_ema = "ESPERA"
if cruce_alcista: status_ema = "ALCISTA"
elif cruce_bajista: status_ema = "BAJISTA"

# --- Visualización ---
st.subheader("Estado del Motor EMA 200")
if status_ema == "ALCISTA": st.success("ALCISTA (Precio > EMA 200)")
elif status_ema == "BAJISTA": st.error("BAJISTA (Precio < EMA 200)")
else: st.warning("ESPERA (En zona de EMA 200)")

# --- Notificación ---
last_saved = get_saved_status()
if status_ema != last_saved and status_ema != "ESPERA":
    send_telegram_msg(f"🚀 OMEGA PRO: El estado ha cambiado a {status_ema}")
    save_status(status_ema)

st.write(f"Precio Actual: {last_close:.2f} | EMA 200: {ema200:.2f}")
