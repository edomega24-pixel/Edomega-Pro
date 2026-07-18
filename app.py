import streamlit as st
import pandas as pd
import time
import requests
import ccxt

# --- CONFIGURACIÓN ---
TOKEN = "8932397018:AAE1etAoCTjdmCP1uLdt01x1DFGaoaT11PE"
CHAT_ID = "7450065212"

# Inicialización
exchange = ccxt.binance({'enableRateLimit': True, 'timeout': 5000})

st.set_page_config(page_title="EDOMEGA PRO - ESTRUCTURA", layout="centered")

st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    .compra {color: #00ff00; font-weight: bold; font-size: 24px;}
    .venta {color: #ff4b4b; font-weight: bold; font-size: 24px;}
    .espera {color: #ffff00; font-weight: bold; font-size: 24px;}
    </style>
""", unsafe_allow_html=True)

st.title("EDOMEGA PRO: Filtro de Estructura de Mercado")

def enviar_alerta(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
        requests.get(url, timeout=5)
    except Exception as e:
        print(f"Error enviando alerta: {e}")

def get_data():
    try:
        ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='5m', limit=250)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except Exception as e:
        print(f"Error en exchange: {e}")
        return None

# --- PRUEBA DE CONEXIÓN ---
enviar_alerta("🚀 EDOMEGA PRO: Prueba de conexión exitosa iniciada.")

placeholder = st.empty()

while True:
    df = get_data()
    
    if df is not None and len(df) >= 200:
        cierre = float(df['close'].iloc[-1])
        volumen_actual = float(df['volume'].iloc[-1])
        volumen_promedio = df['volume'].rolling(20).mean().iloc[-1]
        
        # Filtro de Tendencia: EMA 200
        ema200 = df['close'].ewm(span=200, adjust=False).mean().iloc[-1]
        
        # Indicadores de entrada
        sma = df['close'].rolling(20).mean().iloc[-1]
        std = df['close'].rolling(20).std().iloc[-1]
        bbl = sma - (2.5 * std)
        bbu = sma + (2.5 * std)
        
        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(7).mean()
        loss = (-delta.clip(upper=0)).rolling(7).mean()
        rsi_val = 100 - (100 / (1 + (gain / loss))).iloc[-1]
        
        # --- LÓGICA DE ALTA PRECISIÓN ---
        confirmacion_volumen = volumen_actual > (volumen_promedio * 1.2)
        tendencia_alcista = cierre > ema200
        tendencia_bajista = cierre < ema200
        
        if cierre < bbl and rsi_val < 25 and confirmacion_volumen and tendencia_alcista:
            texto, clase = f"COMPRA (Tendencia Alcista): {cierre:.2f}", "compra"
            enviar_alerta(f"🚀 {texto}")
        elif cierre > bbu and rsi_val > 75 and confirmacion_volumen and tendencia_bajista:
            texto, clase = f"VENTA (Tendencia Bajista): {cierre:.2f}", "venta"
            enviar_alerta(f"📉 {texto}")
        else:
            texto, clase = f"ESPERA (Analizando estructura...)", "espera"
        
        with placeholder.container():
            st.markdown(f"<p class='{clase}'>ESTADO: {texto}</p>", unsafe_allow_html=True)
            st.write(f"Tendencia (EMA 200): {ema200:.2f} | Precio Actual: {cierre:.2f}")
    
    time.sleep(30)