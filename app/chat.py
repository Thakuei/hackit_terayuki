import streamlit as st
import boto3

st.set_page_config(layout="wide")
# def show_redirect_button():
#     st.markdown("本日の面接はこれで終わりです。ありがとうございました。")
#     # 別ページへのボタンを表示
#     if st.button("分析ページに進む"):
#         # ページ遷移を伴う場合は、セッションステートの変更、
#         # やリンクのクリックを促すメッセージを表示
#         st.session_state.redirect = True

def show_chat_page():
    st.write(f'現在ログインしているユーザーは、*{st.session_state["name"]}* です')
    st.success('「面接練習をしたいです」と話しかけてください。')
    
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
        with st.container():
            if message["role"] == "user":
                user_message = st.chat_message("user")
                user_message.write(f"You: {message['content']}")
            elif message["role"] == "bot":
                mensetukan_meaage= st.chat_message("assistant")
                mensetukan_meaage.write(f"bot: {message['content']}")
            # 特定のフレーズが含まれている場合はボタンを表示
                if "本日の面接はこれで終わりです。ありがとうございました" in message['content']:
                    if st.button("分析ページに進む"):
                        st.switch_page("pages/history.py")
                        st.session_state.redirect = True
