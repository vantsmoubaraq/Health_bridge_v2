#!/usr/bin/python3

import requests
from datetime import datetime

access_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjgwMDA2NjMzLCJqdGkiOiI5ZWM0YTU2Yy02MGY3LTRhZTYtYTdhNy1hNThiODQyNzM0ODEiLCJ1c2VyX3V1aWQiOiJhMzk0ZjgxMS1mNjdlLTQyYTMtODcyYS1iYzM4MzU4NzM1YzAifQ.4Iz5ISUjOf0oy5J6HjHTU1kv-sTG2ff2A9w_R6-aGGjcDvNx5qj3BxxRu8WC-055bXTBsAA5QkQAp0uOXNDlmg"

endpoint = "https://api.calendly.com/scheduled_events/e9ed2721-3941-4348-a55f-b511f7617e2f/invitees"
#min_start_time = 

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
#params = {"user": "https://api.calendly.com/users/a394f811-f67e-42a3-872a-bc38358735c0", "min_start_time": "2023-03-02T12:30:00.000000Z"}

response = requests.request("GET", endpoint, headers=headers)

response = response.json()

print(response["collection"][0]["name"])
