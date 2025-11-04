import os
import requests


SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

def send_msg_slack(task):
    json_body = {
        "channel": "C09N95RPR34",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {
        "Authorization": f"Bearer {SLACK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    requests.post(SLACK_URL, json=json_body, headers=headers)