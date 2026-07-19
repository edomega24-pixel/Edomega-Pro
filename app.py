import streamlit as st
import base64
import os

# --- FUNCIÓN DE ALERTAS (Incorporada) ---
def reproducir_alerta(nombre_archivo):
    """
    Reproduce un archivo de audio .mp3 mediante inyección HTML.
    """
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
        # Esto es solo un aviso interno, no altera tu lógica de señales
        pass

# --- AQUÍ VA TODO TU CÓDIGO ORIGINAL SIN MODIFICAR ---
# (Mantén aquí toda tu lógica de cálculo, EMA 200, motor voz, etc.)
# ...
# ...

# --- INTEGRACIÓN DE LAS ALERTAS (Al final de tu lógica de señales) ---

# 1. Alerta prioritaria (Motor Voz + EMA 200)
if condicion_motor_voz and condicion_ema:
    # Mantén aquí tu visualización original (ej: st.markdown, st.write, etc.)
    reproducir_alerta('alerta_especial.mp3') 

# 2. Alerta estándar (Solo Motor Voz)
elif condicion_motor_voz:
    # Mantén aquí tu visualización original
    reproducir_alerta('campana.mp3')
