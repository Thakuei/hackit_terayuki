import streamlit as st
import streamlit_authenticator as stauth

def show_test_page():
    st.write("Welcome to after login page!")
    st.write('Welcome *%s*' % (st.session_state['name']))
    st.title('Some content')
