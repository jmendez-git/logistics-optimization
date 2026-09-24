import urllib.parse
import requests
import streamlit as st


SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

def init_session_state():
    """Init the global vars of the state of the session"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "role" not in st.session_state:
        st.session_state.role = None

def get_login_url() -> str:
    client_id = st.secrets["auth"]["client_id"]
    redirect_uri = st.secrets["auth"]["redirect_uri"]
    
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return auth_url

def authenticate_user(auth_code: str) -> bool:
    try:
        client_id = st.secrets["auth"]["client_id"]
        client_secret = st.secrets["auth"]["client_secret"]
        redirect_uri = st.secrets["auth"]["redirect_uri"]
        
        token_url = "https://oauth2.googleapis.com/token"

        # data
        payload = {
            "code": auth_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        # token access
        token_response = requests.post(token_url, data=payload)
        token_data = token_response.json()
        
        if "error" in token_data:
            st.error(f"Error devuelto por Google: {token_data.get('error_description', token_data['error'])}")
            return False
            
        access_token = token_data.get("access_token")
        
        # get the user information
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_info_response.json()
        
        # save the sesstion state
        st.session_state.authenticated = True
        st.session_state.user_info = user_data
        
        # Roles
        admin_emails = ["joseluismendez.contact@gmail.com"]
        if user_data.get("email") in admin_emails:
            st.session_state.role = "admin"
        else:
            st.session_state.role = "client"
            
        return True

    except Exception as e:
        st.error(f"Error procesando la solicitud de autenticación: {e}")
        return False

def logout():
    """Reboot the user state"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.role = None
    st.rerun()