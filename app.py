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
    </style>
""", unsafe_allow_html=True)

st.title("EDOMEGA PRO: Bot Conectado")
st.write("El bot está funcionando correctamente.")
