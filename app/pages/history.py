import streamlit as st
import boto3
import json

st.title('会話履歴')

# user_input = []
# bot_message = []

#ここからいらないかも
client = boto3.client('logs', region_name='us-east-1')

describe_log_streams_response = client.describe_log_streams(
    logGroupName = 'hackit-terayuki-log',
    orderBy = 'LastEventTime',  # 最後のイベント時間でソート
    descending = True           # 降順
)

# 最初のログストリーム名を取得（最も最近のもの）
log_stream_name = describe_log_streams_response['logStreams'][0]['logStreamName']

# ログイベントを取得
get_log_events_response = client.get_log_events(
    logGroupName = "hackit-terayuki-log",
    logStreamName = log_stream_name,
    startFromHead = True  # 最初からログイベントを取得
)
# ここまでいらないかも

if 'messages' not in st.session_state:
    # 'messages'キーが存在しない場合は初期化します。
    st.session_state['messages'] = []
# # 自分が入力した所の詳細を表示
if st.session_state['messages']:
    for message in st.session_state['messages']:
        with st.container():
            if message["role"] == "user":
                user_message = st.chat_message("user")
                user_message.write(f"You: {message['content']}")
            elif message["role"] == "bot":
                mensetukan_meaage= st.chat_message("assistant")
                mensetukan_meaage.write(f"bot: {message['content']}")
else:
    st.warning("まだ会話履歴がありません。会話をしてください。")
        # # 特定のフレーズが含まれている場合はボタンを表示
        #     if "本日の面接はこれで終わりです。ありがとうございました" in message['content']:
        #         if st.button("分析ページに進む"):
        #             st.switch_page("pages/feedback.py")
        #             st.session_state.redirect = True
# for event in get_log_events_response['events']:
#     st.json(event['message'])
#     user_json_type = json.loads(event['message'])
    
#     if 'inputTranscript' in user_json_type:
#         user_input = user_json_type['inputTranscript']
#         user_message = st.chat_message("user")
#         user_message.write(user_input)

# for event in get_log_events_response['events']:
#     bot_json_type = json.loads(event['message'])

#     if 'messages' in bot_json_type:
#         for message in bot_json_type['messages']:
#             if 'content' in message:
#                 bot_message = message['content']
#                 mensetukan_meaage= st.chat_message("assistant")
#                 mensetukan_meaage.write(bot_message)
# messages = []

# # ユーザーメッセージとボットメッセージの両方に対してタイムスタンプを取得
# for event in get_log_events_response['events']:
#     json_type = json.loads(event['message'])
    
#     # ユーザーメッセージの取得と追加
#     if 'inputTranscript' in json_type:
#         user_input = json_type['inputTranscript']
#         timestamp = event['timestamp']  # タイムスタンプの取得
#         messages.append({'type': 'user', 'text': user_input, 'timestamp': timestamp})
    
#     # ボットメッセージの取得と追加
#     elif 'messages' in json_type:
#         for message in json_type['messages']:
#             if 'content' in message:
#                 bot_message = message['content']
#                 timestamp = event['timestamp']  # タイムスタンプの取得
#                 messages.append({'type': 'bot', 'text': bot_message, 'timestamp': timestamp})

# # タイムスタンプでメッセージをソート
# messages.sort(key=lambda msg: msg['timestamp'])

# # ソートされたメッセージを交互に表示
# for msg in messages:
#     if msg['type'] == 'user':
#         user_message = st.chat_message("user")
#         user_message.write(msg['text'])
#     else:
#         bot_message = st.chat_message("assistant")
#         bot_message.write(msg['text'])
