import streamlit as st
import base64
import os

# 1. FUNCIÓN DE ALERTAS
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

# 2. INICIALIZACIÓN SEGURA (Evita el NameError)
if 'condicion_motor_voz' not in locals():
    condicion_motor_voz = False
if 'condicion_ema' not in locals():
    condicion_ema = False

# 3. AQUÍ VA TU LÓGICA ORIGINAL
# Asegúrate de pegar aquí abajo todo el código que calcula tus señales
# --- COMIENZA TU LÓGICA ---

# [PEGA TU CÓDIGO ORIGINAL AQUÍ]

# --- TERMINA TU LÓGICA ---

# 4. BLOQUE DE ALERTAS (Configurado con tus nombres de archivo actuales)
if condicion_motor_voz and condicion_ema:
    st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
    reproducir_alerta('alerta_especial.mp3.mp3') 
elif condicion_motor_voz:
    st.markdown("### 🔔 Alerta: Motor Voz detectado")
    reproducir_alerta('campana.mp3.mp3')
