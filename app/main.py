#import
import streamlit as st
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader
from pages.test import show_test_page

#ログイン認証
with open("config/config.yaml", "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

# st.session_stateに変える
if st.session_state['authentication_status']:
    show_test_page()
elif st.session_state['authentication_status'] == False:
    st.error('ユーザーネームまたはパスワードが違います。再度入力してください。')
elif st.session_state['authentication_status'] == None:
    st.info('ユーザーネームとパスワードを入力してください。')
