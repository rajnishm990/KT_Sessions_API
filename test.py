import requests
import time
import json

BASE_URL = "http://localhost:8000"

# ---- 1. Login to get JWT token ----
LOGIN_URL = f"{BASE_URL}/api/token/"
login_payload = {
    "username": "testuser",  #use the credentials from superuser or a user created through admin panel
    "password": "password"  
}
response = requests.post(LOGIN_URL, json=login_payload)
print("Login Response:", response.status_code, response.json())

access_token = response.json().get("access")
headers = {"Authorization": f"Bearer {access_token}"}

#2. Create a KT Session 
session_payload = {
    "title": "React Hooks Knowledge Transfer",
    "description": "Session covering useState, useEffect, and custom hooks"
}
response = requests.post(f"{BASE_URL}/api/kt/", json=session_payload, headers=headers)
print("Create Session:", response.status_code, response.json())

#3. List User Sessions to get session ID 
response = requests.get(f"{BASE_URL}/api/kt/", headers=headers)
print("List Sessions:", response.status_code, response.json())
sessions = response.json()
session_id = sessions['results'][0].get('id') if sessions else None

# 4. Get Session Details ----
if session_id:
    response = requests.get(f"{BASE_URL}/api/kt/{session_id}/", headers=headers)
    print("Session Details:", response.status_code, response.json())

# 5. Add Attachment to Session
    attachment_payload = {
        "file_type": "audio"
    }
    response = requests.post(
        f"{BASE_URL}/api/kt/{session_id}/add_attachment/",
        data=attachment_payload,
        headers=headers
    )
    print("Add Attachment:", response.status_code, response.json())
    attachment_id = response.json().get('id')



#6. View Shared Session (Public)
if session_id:
    response = requests.get(f"{BASE_URL}/api/kt/{session_id}/", headers=headers)
    session_detail = response.json()
    share_url = session_detail.get("share_url") or 'None'
    response = requests.get(share_url)
    print("Shared Session:", response.status_code, response.json())

time.sleep(3)

#7. Get Attachment Details
detail_response = requests.get(f"{BASE_URL}/api/attachments/{attachment_id}/", headers=headers)
print("Attachment Details:", detail_response.status_code, detail_response.json())