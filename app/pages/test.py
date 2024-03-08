import streamlit as st
import streamlit_authenticator as stauth

def show_test_page():
    st.write(f'現在ログインしているユーザーは、*{st.session_state["name"]}* です')
    st.title('Some content')
