import requests
import json
import base64
import os
from utils import load_tokens, save_tokens, refresh_access_token

# Function to schedule a meeting
def schedule_meeting(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    meeting_details = {
        "topic": "Automated Meeting",
        "type": 2,
        "start_time": "2024-06-13T07:20:00Z",
        "duration": 60,
        "timezone": "UTC",
        "agenda": "This is an automated meeting",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "watermark": True,
            "use_pmi": False,
            "approval_type": 0,
            "registration_type": 1,
            "audio": "both",
            "auto_recording": "cloud"
        }
    }
    
    user_id = 'me'
    response = requests.post(f'https://api.zoom.us/v2/users/{user_id}/meetings', headers=headers, json=meeting_details)
    
    if response.status_code == 201:
        meeting = response.json()
        join_url = meeting.get('join_url')
        return join_url
    else:
        return None

# Main function to be executed
def main():
    tokens = load_tokens()
    
    if 'access_token' in tokens:
        access_token = tokens['access_token']
        join_url = schedule_meeting(access_token)
        if join_url:
            print("Meeting scheduled successfully!")
            print("Join URL:", join_url)
        else:
            print("Failed to schedule meeting.")
    else:
        print("No access token found. Make sure to obtain one.")

if __name__ == "__main__":
    main()
