#!/usr/bin/python3

import requests
from datetime import datetime, timedelta, timezone

access_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjgwMDA2NjMzLCJqdGkiOiI5ZWM0YTU2Yy02MGY3LTRhZTYtYTdhNy1hNThiODQyNzM0ODEiLCJ1c2VyX3V1aWQiOiJhMzk0ZjgxMS1mNjdlLTQyYTMtODcyYS1iYzM4MzU4NzM1YzAifQ.4Iz5ISUjOf0oy5J6HjHTU1kv-sTG2ff2A9w_R6-aGGjcDvNx5qj3BxxRu8WC-055bXTBsAA5QkQAp0uOXNDlmg"

endpoint = "https://api.calendly.com/scheduled_events"

# Get the current UTC datetime
now = datetime.utcnow()

# Set the minimum start time to be a week ago
min_start_time = now - timedelta(days=7)

# Convert the minimum start time to UTC timezone
min_start_time_utc = min_start_time.replace(tzinfo=timezone.utc)

# Print the minimum start time in ISO 8601 format
min_start_time = min_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
params = {"user": "https://api.calendly.com/users/a394f811-f67e-42a3-872a-bc38358735c0", "min_start_time": min_start_time}

response = requests.get(endpoint, headers=headers, params=params)
response = response.json()

def events(response):
    """returns all events in last 7 days"""
    event_details = []

    for event in response["collection"]:
        uri = event["uri"]
        uri = uri.split("/")[4]
        location = event["location"].get("join_url", None)
        name = event["name"]
        start_time = event["start_time"]
        status = event["status"]
        event_details.append({"uri": uri, "location": location, "name": name, "start_time": start_time, "status": status})
    return(event_details)

all_events = events(response)

def invitees(all_events, headers):
    invitee_ids = []
    for event in all_events:
        invitee_ids.append(event["uri"])

    invitee_details = []
    for invitee_id in invitee_ids:
        invitee_url = f"https://api.calendly.com/scheduled_events/{invitee_id}/invitees"
        r = requests.get(invitee_url, headers=headers)
        r = r.json()
        if "collection" in r:
            user_name = r.get("collection", None)[0]["name"]
            user_email = r.get("collection", None)[0]["email"]
            invitee_details.append({invitee_id: {"user_name": user_name, "user_email": user_email}})
    return(invitee_details)

all_invitees = invitees(all_events, headers)

for event in all_events:
    for invitee in all_invitees:
        if event["uri"] in invitee:
            event.update(invitee[event["uri"]])

print(all_events)
