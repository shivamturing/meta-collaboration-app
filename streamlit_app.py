import streamlit as st
from streamlit_google_auth import Authenticate
import json

# Load secrets
google_credentials = {
    "web": {
        "client_id": st.secrets["google_auth"]["client_id"],
        "project_id": st.secrets["google_auth"]["project_id"],
        "auth_uri": st.secrets["google_auth"]["auth_uri"],
        "token_uri": st.secrets["google_auth"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google_auth"]["auth_provider_x509_cert_url"],
        "client_secret": st.secrets["google_auth"]["client_secret"],
        "redirect_uris": st.secrets["google_auth"]["redirect_uris"].split(","),
        "javascript_origins": st.secrets["google_auth"]["javascript_origins"].split(",")
    }
}

# Save credentials to a temporary file
with open('google_credentials_temp.json', 'w') as f:
    json.dump(google_credentials, f)

# Initialize the Authenticate class
authenticator = Authenticate(
    secret_credentials_path='google_credentials_temp.json',
    cookie_name=st.secrets["environment"]["cookie_name"],
    cookie_key=st.secrets["environment"]["cookie_key"],
    redirect_uri=st.secrets["environment"]["redirect_uri"],
)

# Check if the user is already authenticated
authenticator.check_authentification()

# Display the login button if the user is not authenticated
if not st.session_state.get('connected', False):
    authorization_url = authenticator.get_authorization_url()
    st.markdown(f'[Login]({authorization_url})')
    st.link_button('Login', authorization_url)
# Display the user information and logout button if the user is authenticated
else:
    st.image(st.session_state['user_info'].get('picture'))
    st.write(f"Hello, {st.session_state['user_info'].get('name')}")
    st.write(f"Your email is {st.session_state['user_info'].get('email')}")
    if st.button('Log out'):
        authenticator.logout()
