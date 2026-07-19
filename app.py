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

# 2. TU LÓGICA ORIGINAL (AQUÍ DEBE APARECER TODO)
# [PEGA AQUÍ TU LÓGICA COMPLETA DE PRECIOS, GRÁFICOS Y VARIABLES]

# 3. BLOQUE DE ALERTAS (PROTEGIDO)
# Solo verificamos variables si ya existen para no romper el script
c_voz = globals().get('condicion_motor_voz', False)
c_ema = globals().get('condicion_ema', False)

if c_voz and c_ema:
    st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
    reproducir_alerta('alerta_especial.mp3.mp3') 
elif c_voz:
    st.markdown("### 🔔 Alerta: Motor Voz detectado")
    reproducir_alerta('campana.mp3.mp3')
