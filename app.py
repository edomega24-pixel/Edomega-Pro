import streamlit as st
import base64
import os

# --- SISTEMA DE ALERTAS (NUEVO) ---
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

# --- INICIALIZACIÓN DE SEGURIDAD (PARA EVITAR EL ERROR DE PANTALLA NEGRA) ---
if 'condicion_motor_voz' not in locals():
    condicion_motor_voz = False
if 'condicion_ema' not in locals():
    condicion_ema = False

# --- TU LÓGICA ORIGINAL (INTACTA) ---
# Aquí es donde funciona todo tu sistema original. 
# No he cambiado ni un solo cálculo, condición o configuración.
# Pega TODO tu código justo debajo de esta línea:

# [PEGA AQUÍ TU LÓGICA ORIGINAL COMPLETA]


# --- BLOQUE DE ALERTAS (INTEGRADO AL FINAL) ---
# Este bloque solo actúa cuando tus bots ya hicieron su trabajo.
if condicion_motor_voz and condicion_ema:
    st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
    reproducir_alerta('alerta_especial.mp3.mp3') 
elif condicion_motor_voz:
    st.markdown("### 🔔 Alerta: Motor Voz detectado")
    reproducir_alerta('campana.mp3.mp3')
