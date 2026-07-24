CHAT_ID = "7450065212"
STATUS_FILE = "status.txt"

# --- JavaScript para Auto-Refresh ---
# Esto le dice al navegador que recargue la página cada 30 segundos
st.markdown("""
    <meta http-equiv="refresh" content="30">
""", unsafe_allow_html=True)

# --- Funciones de Gestión ---
# Caché ajustada a 20s para mayor frescura de datos
@st.cache_data(ttl=20)
def get_market_data():
ticker = yf.Ticker("BTC-USD")
    # Intervalo de 1 minuto para mayor precisión de broker
return ticker.history(period="1d", interval="1m")

def get_saved_status():
@@ -30,12 +34,11 @@ def send_telegram_msg(text):
requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

st.set_page_config(page_title="OMEGA PRO", layout="wide")
st.title("🚀 OMEGA PRO: Panel Maestro en Tiempo Real")
st.title("🚀 OMEGA PRO: Monitoreo Autónomo")

# --- Obtención de Datos ---
df = get_market_data()
last_close = df['Close'].iloc[-1]
# Cálculo de EMA 200 y rangos BOS basados en el nuevo intervalo de 1 minuto
ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
high_prev = df['High'].iloc[-26:-1].max()
low_prev = df['Low'].iloc[-26:-1].min()
@@ -58,15 +61,10 @@ def send_telegram_msg(text):
elif status_ema == "BAJISTA": st.error("BAJISTA")
else: st.warning("ESPERA")

# --- Botón de Refresco Manual ---
if st.button("🔄 Refrescar Mercado"):
    st.rerun()

# --- Notificación y Sinergia ---
current_total_status = f"{status_bos}_{status_ema}"
last_saved = get_saved_status()

# Alerta de Sinergia Púrpura si ambos coinciden
if (status_bos == "COMPRA" and status_ema == "ALCISTA") or (status_bos == "VENTA" and status_ema == "BAJISTA"):
st.markdown("""<div style="background-color: purple; color: white; padding: 20px; border-radius: 10px; text-align: center;">🔥 SINERGIA TOTAL ALINEADA 🔥</div>""", unsafe_allow_html=True)

@@ -76,4 +74,4 @@ def send_telegram_msg(text):

st.divider()
st.write(f"**Precio Actual:** {last_close:.2f} | **EMA 200:** {ema200:.2f}")
st.caption("Sistema optimizado para actualizaciones cada 20 segundos.")
st.caption("El sistema se actualiza automáticamente cada 30 segundos. ¡No necesitas hacer nada!")
