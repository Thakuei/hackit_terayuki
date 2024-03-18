import streamlit as st
import boto3
from audio_recorder_streamlit import audio_recorder
from botocore.exceptions import NoCredentialsError
import time
import json
from datetime import datetime
from transcribe import trans_function
import requests
import os

st.set_page_config(layout="wide")

#voicevoxのAPI設定
VOILCEVOX_API_URL = os.getenv('VOICE_API_URL', 'http://localhost:50021')

def synthesize_voice(text='text', speaker_id=8):
    # 音声合成のクエリを生成
    query_response = requests.post(
        f'{VOILCEVOX_API_URL}/audio_query',
        params ={('text', text), ("speaker", speaker_id)}
    )
    query = query_response.json()

    # 音声を合成
    synthesis_response = requests.post(
        f'{VOILCEVOX_API_URL}/synthesis',
        headers={"Content-Type": "application/json"},
        params ={('text', text), ("speaker", speaker_id)}, 
        data=json.dumps(query)
    )
    audio_data = synthesis_response.content
    return audio_data

def show_chat_page():
    trans_function()
    st.write(f'現在ログインしているユーザーは、*{st.session_state["name"]}* です')
    st.success('「面接練習をしたいです」と話しかけてください。')
    col1, col2 = st.columns([2, 5])
    with col1:
        st.image("img/office-tr.gif")
    with col2:
        st.code('面接練習をしたいです')
    
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
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    if message["role"] == "user":
                        user_message = st.chat_message("user", avatar="🧑🏻‍💻")
                        user_message.write(f"You: {message['content']}")
                    elif message["role"] == "bot":
                        mensetukan_meaage= st.chat_message("assistant", avatar="👩")
                        mensetukan_meaage.write(f"bot: {message['content']}")
                with col2:
                    if message["role"] == "bot":
                        play_audio = st.button("📢",key=message['content'])
                        if play_audio:
                            audio_data = synthesize_voice(message['content'])
                            st.audio(audio_data, format='audio/wav')
                    # 特定のフレーズが含まれている場合はボタンを表示
                        if "本日の面接はこれで終わりです。ありがとうございました" in message['content']:
                            if st.button("分析ページに進む"):
                                st.switch_page("pages/history.py")
                                st.session_state.redirect = True