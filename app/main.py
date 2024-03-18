#import
import streamlit as st
import streamlit_authenticator as stauth
import yaml 
from yaml.loader import SafeLoader
from chat import show_chat_page
import os

st.title('面接シミュレーション')

# カレントディレクトリのパスを取得
current_directory = os.getcwd()

# config.yaml へのフルパスを生成
config_path = os.path.join(current_directory, "./config.yaml")

# フルパスを使用してファイルを開く
with open(config_path, "r") as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

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
