import streamlit as st

user = st.session_state.user_info
st.title("🧑‍🎓 Panel de Administración")
st.success(f"Bienvenido Administrador: {user.get('name')} ({user.get('email')})")

st.metric(label="Flotas Registradas", value="8")
st.metric(label="Costo de Operación Promedio", value="$1,240 MXN/día")