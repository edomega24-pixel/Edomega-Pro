import streamlit as st
import base64
import os

# --- 1. FUNCIÓN DE ALERTAS ---
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

# --- 2. INICIALIZACIÓN DE VARIABLES ---
# Definimos las variables antes de usarlas para que no den error
condicion_motor_voz = False
condicion_ema = False

# --- 3. TU LÓGICA ORIGINAL ---
# (Aquí es donde debes tener el resto de tu código que calcula las condiciones)
# ... todo tu código original va aquí ...


# --- 4. BLOQUE DE ALERTAS (Ya no dará error porque las variables ya existen) ---
if condicion_motor_voz and condicion_ema:
    st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
    reproducir_alerta('alerta_especial.mp3')
elif condicion_motor_voz:
    st.markdown("### 🔔 Alerta: Motor Voz detectado")
    reproducir_alerta('campana.mp3')
