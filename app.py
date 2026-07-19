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
    else:
        st.warning(f"Archivo de audio no encontrado: {nombre_archivo}")

# --- 2. AQUÍ EMPIEZA TU LÓGICA ORIGINAL ---
# COPIA Y PEGA AQUÍ TODO TU CÓDIGO DONDE CALCULAS TUS VARIABLES
# Asegúrate de que al final de tu lógica queden definidas:
# condicion_motor_voz = ...
# condicion_ema = ...
# -------------------------------------------

### AQUÍ PEGA TU LÓGICA DE CÁLCULO DE SEÑALES ###


# --- 3. BLOQUE DE ALERTAS (Debe ir al final para detectar las variables) ---
# Usamos 'try' para evitar errores si las variables no se definieron por alguna razón
try:
    if 'condicion_motor_voz' in locals() and 'condicion_ema' in locals():
        if condicion_motor_voz and condicion_ema:
            st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
            reproducir_alerta('alerta_especial.mp3')
        elif condicion_motor_voz:
            st.markdown("### 🔔 Alerta: Motor Voz detectado")
            reproducir_alerta('campana.mp3')
except Exception as e:
    st.error(f"Error en la lógica de alertas: {e}")
