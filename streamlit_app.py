import streamlit as st
from streamlit_google_auth import Authenticate

# Initialize the Authenticate class
authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri='http://localhost:8501',
)

# Check if the user is already authenticated
authenticator.check_authentification()

# Display the login button if the user is not authenticated
if not st.session_state.get('connected', False):
    authorization_url = authenticator.get_authorization_url()
    st.markdown(f'[Login]({authorization_url})')
    st.button('Login', on_click=lambda: st.experimental_rerun())
else:
    # Display the user information and logout button
    st.image(st.session_state['user_info'].get('picture'))
    st.write(f"Hello, {st.session_state['user_info'].get('name')}")
    st.write(f"Your email is {st.session_state['user_info'].get('email')}")
    if st.button('Log out'):
        authenticator.logout()
        st.experimental_rerun()