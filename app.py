import streamlit as st
from core.trip import Trip
from utils.config import load_config

st.set_page_config(page_title="Taxímetro", page_icon="🚕", layout="centered")

if "trip" not in st.session_state:
    st.session_state.trip = Trip()

if "config" not in st.session_state:
    st.session_state.config = load_config()

if "last_result" not in st.session_state:
    st.session_state.last_result = None  

trip = st.session_state.trip
config = st.session_state.config

STOPPED_RATE = float(config.get("stopped_rate", 0.02))
MOVING_RATE = float(config.get("moving_rate", 0.05))


def calc_fare(stopped_s: float, moving_s: float) -> float:
    return stopped_s * STOPPED_RATE + moving_s * MOVING_RATE


def estado_legible(t: Trip) -> str:
    if not t.active:
        return "Sin trayecto"
    return "Parado" if t.state == "stopped" else "En marcha"


def etiqueta_paso(t: Trip) -> str:
    if not t.active:
        return "Iniciar"
    if t.state == "stopped":
        return "Poner en marcha"
    return "Detener (o finalizar)"


can_start = not trip.active
can_move = trip.active and trip.state == "stopped"
can_stop = trip.active and trip.state == "moving"
can_finish = trip.active

def iniciar():
    try:
        trip.start()
        st.session_state.last_result = None
        st.toast("Trayecto iniciado", icon="🚕")
    except RuntimeError:
        st.warning("Ya hay un trayecto en curso.")


def poner_en_marcha():
    try:
        trip.change_state("moving")
        st.toast("En marcha", icon="🚗")
    except RuntimeError:
        st.warning("No hay un trayecto activo. Pulsa 'Iniciar'.")


def detener():
    try:
        trip.change_state("stopped")
        st.toast("Taxi detenido", icon="⏸️")
    except RuntimeError:
        st.warning("No hay un trayecto activo. Pulsa 'Iniciar'.")


def finalizar():
    try:
        stopped_s, moving_s = trip.finish()
        total = calc_fare(stopped_s, moving_s)
        st.session_state.last_result = (stopped_s, moving_s, total)
        st.toast("Trayecto finalizado", icon="🏁")
    except RuntimeError:
        st.warning("No hay un trayecto activo para finalizar.")


st.title("🚕 Taxímetro")
st.caption("Controla el trayecto de tu viaje y visualiza el total en tiempo real.")

total_actual = calc_fare(trip.stopped_seconds, trip.moving_seconds)

k1, k2, k3 = st.columns(3)
k1.metric("Estado", estado_legible(trip))
k2.metric("Total actual (€)", f"{total_actual:.2f}")
k3.metric("Siguiente acción", etiqueta_paso(trip))

st.divider()

st.subheader("Controles")
st.write("Usa los botones en orden. Puedes alternar **En marcha** / **Detener** las veces que quieras.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.button("▶️ Iniciar", on_click=iniciar, disabled=not can_start, use_container_width=True)
with c2:
    st.button("🚗 En marcha", on_click=poner_en_marcha, disabled=not can_move, use_container_width=True)
with c3:
    st.button("⏸️ Detener", on_click=detener, disabled=not can_stop, use_container_width=True)
with c4:
    st.button("🏁 Finalizar", on_click=finalizar, disabled=not can_finish, use_container_width=True)

st.divider()

st.subheader("Detalle del trayecto")
d1, d2 = st.columns(2)
d1.metric("Tiempo parado (s)", f"{trip.stopped_seconds:.1f}")
d2.metric("Tiempo en marcha (s)", f"{trip.moving_seconds:.1f}")

with st.expander("Ver tarifas actuales"):   
    st.write(f"⏱️ Parado: **{STOPPED_RATE:.3f} €/s**")
    st.write(f"🚗 En marcha: **{MOVING_RATE:.3f} €/s**")

if st.session_state.last_result:
    stopped_s, moving_s, total = st.session_state.last_result
    st.success("Resumen del trayecto")
    r1, r2, r3 = st.columns(3)
    r1.metric("Parado (s)", f"{stopped_s:.1f}")
    r2.metric("En marcha (s)", f"{moving_s:.1f}")
    r3.metric("Total (€)", f"{total:.2f}")
