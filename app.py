import streamlit as st
import base64
import os

# 1. FUNCIÓN DE ALERTAS (Debe ir al principio)
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

# 2. TU LÓGICA ORIGINAL COMPLETA
# Pega aquí todo, ABSOLUTAMENTE TODO, lo que tenías programado antes.
# Asegúrate de que las variables 'condicion_motor_voz' y 'condicion_ema'
# se definan en algún punto de este código original.

# --- INICIO DE TU CÓDIGO ---
# [PEGA TODO TU CÓDIGO AQUÍ]
# --- FIN DE TU CÓDIGO ---

# 3. BLOQUE DE ALERTAS (Al final, para que pueda leer las variables definidas arriba)
# Usamos 'try' para que si algo falla, no bloquee la aplicación completa.
try:
    if 'condicion_motor_voz' in locals() and condicion_motor_voz:
        if 'condicion_ema' in locals() and condicion_ema:
            st.markdown("### 🚀 ALERTA PÚRPURA: MOTOR VOZ + EMA 200")
            reproducir_alerta('alerta_especial.mp3.mp3')
        else:
            st.markdown("### 🔔 Alerta: Motor Voz detectado")
            reproducir_alerta('campana.mp3.mp3')
except Exception as e:
    st.error(f"Error en el bloque de alertas: {e}")
