import streamlit as st
import boto3

st.write('You are happy boy so no attention is needed')
    # client = boto3.client('logs', region_name='us-east-1')

    # response = client.get_log_event(
    #     logGroupName = 'hackit-terayuki-log',
    #     logStreamName = '',
    #     startFromHead = False,
    #     limit=1
    # )

    # if response['events']:
    #     latest_event = response['events'][0]
    #     print(latest_event['message'])
    # else:
    #     print('No logs found')
