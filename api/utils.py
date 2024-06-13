import json
import os
import requests
import base64

# Function to load tokens from a file
def load_tokens():
    token_file = 'zoom_tokens.json'
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return json.load(f)
    return {}

# Function to save tokens to a file
def save_tokens(tokens):
    token_file = 'zoom_tokens.json'
    with open(token_file, 'w') as f:
        json.dump(tokens, f)

# Function to refresh the access token
def refresh_access_token(refresh_token):
    client_id = os.getenv('ZOOM_CLIENT_ID')
    client_secret = os.getenv('ZOOM_CLIENT_SECRET')
    
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response_data = response.json()
    if 'access_token' in response_data:
        save_tokens(response_data)  
        return response_data.get("access_token")
    else:
        print("Failed to refresh access token.")
        return None
