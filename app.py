import streamlit as st
from services import auth

st.set_page_config(
    page_title="DSS Vanthora - Optimización de Rutas",
    page_icon="🚚",
    layout="wide"
)

auth.init_session_state()

# Get the response from Google OAuth
query_params = st.query_params
if "code" in query_params and not st.session_state.authenticated:
    auth_code = query_params["code"]
    with st.spinner("Verificando cuenta de Google..."):
        if auth.authenticate_user(auth_code):
            st.query_params.clear()
            st.rerun()


def index():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("🚚 DSS Vanthora")
        st.subheader("Optimización de Rutas")
        st.divider()
        st.write("Por favor, inicia sesión con tu cuenta de Google para acceder.")
        
        login_url = auth.get_login_url()
        
        st.markdown(
            f'''
            <a href="{login_url}" target="_self">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;">
                    Iniciar sesión con Google
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )

def logout_action():
    auth.logout()

page_logout = st.Page(logout_action, title="Cerrar Sesión", icon="👈")

page_admin = st.Page(
    "pages/admin.py",
    title="Panel de Administración",
    icon="🚀",
    default=True
)

page_client = st.Page(
    "pages/client.py",
    title="Optimización de Rutas",
    icon="📊",
    default=True
)

st.logo("🚚")

if not st.session_state.authenticated: # not authenticated
    pg = st.navigation([st.Page(index, title="Inicio", icon="🔑")])
else:
    # navigation rol services/auth.py
    user_role = st.session_state.role
    
    if user_role == "admin":
        nav_structure = {
            "Administración": [page_admin],
            "Cuenta": [page_logout]
        }
    else:  # Cliente / Operador
        nav_structure = {
            "Servicios": [page_client],
            "Cuenta": [page_logout]
        }
        
    pg = st.navigation(nav_structure)

pg.run()