import streamlit as st
import boto3
from audio_recorder_streamlit import audio_recorder
from botocore.exceptions import NoCredentialsError
import time
import json
from datetime import datetime



def trans_function():
#==========================基本情報=======================================
    # s3クライアント
    s3_client = boto3.client('s3',region_name='us-east-1')

    # transcribe設定
    transcribe_client = boto3.client('transcribe',region_name='us-east-1')

    # 保存するファイル名を指定
    file_name = "recorded_audio.wav"

    # s3のURI
    uri = "s3://hackit-terayuki.pk/recorded_audio.wav"
#========================================================================
    
    #録音するとこ
    with st.sidebar:
        audio_bytes = audio_recorder(
        text="",
        recording_color="#ff0000",
        neutral_color="#ffffff",
        icon_name="microphone-lines",
        icon_size="3x",
        )
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

    # 撮った音声をファイル保存
    def save_audio_file(audio_bytes, file_name):
        with open(file_name, 'wb') as audio_file:
            audio_file.write(audio_bytes)
    
    # s3に保存
    def upload_file_to_s3(file_name, bucket_name):
        try:
            s3_client.upload_file(file_name, bucket_name, file_name)
            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False
        
    def transcribe():

        if not audio_bytes:
            # `audio_bytes`がない場合、メッセージを表示して関数から抜ける
            st.warning("録音された音声がありません")
            return  # 関数の実行をここで停止

        # `st.empty()`を使用してプレースホルダを作成
        processing_placeholder = st.empty()
        processing_placeholder.write("Still processing...")

        
        # 録音データをファイルに保存
        save_audio_file(audio_bytes, file_name)
        
        # S3バケット名を指定
        bucket_name = "hackit-terayuki.pk"
        
        # ファイルをS3にアップロード
        upload_success = upload_file_to_s3(file_name, bucket_name)
        if upload_success:
            print("File successfully uploaded to S3.")
        else:
            print("File upload to S3 failed.")


#------------------------------------transcribeで文字にしてもらう-----------------------

        # 初期の文字列
        job_name = "transcrioted-terayuki"

        # 現在の日時を YYYYMMDD_HHMMSS 形式で取得
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 現在の日時を元の文字列に追加
        job_name = f"{job_name}_{current_time}"

        s3_uri = uri  # S3の音声ファイルURI
        output_bucket_name = "hackit-terayuki.pk"  # 結果を保存するS3バケット名

        # 音声をテキストに変換するジョブを開始
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='wav',  # あなたのファイルフォーマットに合わせて変更してください
            LanguageCode='ja-JP',  # 音声の言語コード
            OutputBucketName=output_bucket_name
        )

        # processing_displayed = False
        
        # while True:
        #     status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        #     if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        #         break
        #     if not processing_displayed:
        #         st.write("Still processing...")
        #         processing_displayed = True
        #     time.sleep(5)

        while True:
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(5)

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            # 結果のファイルパスを取得
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

            # S3バケット名とファイルキーの抽出
            bucket_name = "hackit-terayuki.pk"
            key = f"{job_name}.json"
            
            # ダウンロードするファイルの名前を指定
            download_path = 'transcribed_text.json'

            #st.text(bucket_name)
            #st.text(key)

            s3_client.download_file(bucket_name, key, download_path)

            # 処理が終了したので、"Still processing..."のメッセージを消去
            processing_placeholder.empty()

            # ファイルを開いて内容を読み込む
            with open(download_path, 'r') as file:
                transcribed_text = json.load(file)

            # Streamlitを使用して結果を表示
            transcript = transcribed_text['results']['transcripts'][0]['transcript']

            st.code(transcript)

        #else:
            #st.write("正常に動作しました")

#------------------------------------------------------------------------------------


    with st.sidebar:

        if st.button('音声のテキスト化'):
            transcribe() 
        
