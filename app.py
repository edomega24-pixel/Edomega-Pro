import streamlit as st
import yfinance as yf
import requests
import base64
import os

# --- CONFIGURACIÓN ---
CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"
TOKEN = "7722650058:AAH47uRk5a-GjV8v06t0BqZ2pXzW41rT22w" # Asegúrate de tener tu token aquí

# --- FUNCIÓN DE ALERTAS ---
def reproducir_alerta(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'''
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            '''
            st.markdown(audio_html, unsafe_allow_html=True)

# --- AUTO-REFRESH ---
st.markdown('<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)

# --- FUNCIONES DE GESTIÓN ---
@st.cache_data(ttl=20)
def get_market_data():
    ticker = yf.Ticker("BTC-USD")
    return ticker.history(period="1d", interval="1m")

def get_saved_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read()
    return ""

def send_telegram_msg(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.set_page_config(page_title="OMEGA PRO", layout="wide")
st.title("🚀 OMEGA PRO: Monitoreo Autónomo")

# --- OBTENCIÓN DE DATOS ---
df = get_market_data()
last_close = df['Close'].iloc[-1]
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()

# --- LÓGICA DE VARIABLES (PARA ALERTAS) ---
# Definimos las variables para que el bloque de abajo las lea
condicion_motor_voz = False # Aquí irá tu lógica de BOS si aplica
condicion_ema = False

# Cálculo de estados
if last_close > high_prev:
    status_bos = "COMPRA"
    condicion_motor_voz = True
elif last_close < low_prev:
    status_bos = "VENTA"
    condicion_motor_voz = True
else:
    status_bos = "ESPERA"

if last_close > ema200:
    status_ema = "ALCISTA"
    condicion_ema = True
elif last_close < ema200:
    status_ema = "BAJISTA"
    condicion_ema = True
else:
    status_ema = "ESPERA"

# Visualización
st.write(f"**BOS:** {status_bos} | **EMA 200:** {status_ema}")

# --- NOTIFICACIÓN Y SINERGIA ---
if (status_bos == "COMPRA" and status_ema == "ALCISTA") or (status_bos == "VENTA" and status_ema == "BAJISTA"):
    st.markdown("""<div style="background-color: purple; color: white; padding: 20px; border-radius: 10px; text-align: center;">🔥 SINERGIA TOTAL ALINEADA 🔥</div>""", unsafe_allow_html=True)
    reproducir_alerta('alerta_especial.mp3.mp3') # Alerta especial
elif condicion_motor_voz:
    reproducir_alerta('campana.mp3.mp3') # Alerta estándar

st.divider()
st.write(f"**Precio Actual:** {last_close:.2f} | **EMA 200:** {ema200:.2f}")
st.caption("El sistema se actualiza automáticamente cada 30 segundos.")
