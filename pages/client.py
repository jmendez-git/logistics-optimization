import streamlit as st

user = st.session_state.user_info
st.title("🤖 Módulo de Optimización de Rutas (VRP)")
st.info(f"Sesión activa como Cliente: {user.get('name')}")

st.write("Carga los puntos de entrega en CSV o selecciona nodos en el mapa para calcular la ruta óptima.")