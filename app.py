import streamlit as st

st.title('Vanthora')

# Verificar si el usuario ha iniciado sesión
if not st.user.is_logged_in:
    st.write("Por favor, inicia sesión para acceder al contenido.")
    
    # Botón nativo de inicio de sesión
    if st.button("Iniciar sesión con Google"):
        st.login()
else:
    # El usuario ya está autenticado
    st.success(f"¡Bienvenido, {st.user.name}!")
    
    # Mostrar datos del perfil del usuario si lo deseas
    st.write(f"Tu correo electrónico es: {st.user.email}")
    if st.user.picture:
        st.image(st.user.picture, width=100)
    
    st.divider()
    st.write("Aquí va el contenido exclusivo de tu aplicación...")
    
    # Botón nativo para cerrar sesión
    if st.button("Cerrar sesión"):
        st.logout()