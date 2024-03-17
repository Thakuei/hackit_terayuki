#import
import streamlit as st
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader
from chat import show_chat_page

st.title('面接シミュレーション')

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

if st.session_state['authentication_status']:
    show_chat_page()
    with st.sidebar:
        st.write("---------")
        authenticator.logout("ログアウト")
elif st.session_state['authentication_status'] == False:
    st.error('ユーザーネームまたはパスワードが違います。再度入力してください。')
elif st.session_state['authentication_status'] == None:
    st.info('ユーザーネームとパスワードを入力してください。')
