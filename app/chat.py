import streamlit as st
import boto3

def show_chat_page():
    st.write(f'現在ログインしているユーザーは、*{st.session_state["name"]}* です')
    st.write('「面接練習をしたいです」と話しかけてください。')
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    user_input = st.chat_input('ここに入力してください')

    #v2のクライアントを作成
    lex_v2_client = boto3.client('lexv2-runtime', region_name='us-east-1')
    
    if user_input:
        
        st.session_state['messages'].append({"role": "user", "content": user_input})
        
        response = lex_v2_client.recognize_text(
            botId='SQRIB4YMIT', # ボットIDを指定
            botAliasId='QVZTE6FNSP',  # エイリアスIDを指定
            localeId='ja_JP',  # 対象のロケールID（例: 'ja_JP'）
            sessionId=st.session_state["name"],  # 一意のセッションIDを指定
            text=user_input
        )
        
        if response['messages']:
            lex_response = response['messages'][0]['content']
            st.session_state['messages'].append({"role": "bot", "content": lex_response})
    
    for message in st.session_state['messages']:
    # Display the message in the chat box with appropriate role
        with st.container():
            if message["role"] == "user":
                st.write(f"You: {message['content']}")
            else:
                st.write(f"bot: {message['content']}")