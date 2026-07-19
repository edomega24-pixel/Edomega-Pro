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

# 2. AQUÍ VA TODO TU CÓDIGO ORIGINAL (Lógica de señales, cálculos, etc.)
# --- COMIENZA TU LÓGICA ---
# [PEGA AQUÍ TODO EL CÓDIGO QUE YA TENÍAS ANTES]
# --- TERMINA TU LÓGICA ---

# 3. VERIFICACIÓN Y ALERTAS (Esto va al final de todo)
# Usamos 'globals().get' para evitar el NameError si la variable no existe
cond_voz = globals().get('condicion_motor_voz', False)
cond_ema = globals().get('condicion_ema', False)

if cond_voz and cond_ema:
    st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
    reproducir_alerta('alerta_especial.mp3')
elif cond_voz:
    st.markdown("### 🔔 Alerta: Motor Voz detectado")
    reproducir_alerta('campana.mp3')
