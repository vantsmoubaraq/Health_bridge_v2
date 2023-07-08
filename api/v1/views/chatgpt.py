#!/usr/bin/env python3

from flask import request, jsonify, abort
import requests

from api.v1.views import ui

@ui.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Get the JSON data from the request
    message = data['message']  # Extract the user's message

    # Call the ChatGPT API
    response = call_chatgpt_api(message)

    return jsonify({'response': response})

def call_chatgpt_api(message):
    api_key = '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'
    endpoint = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
         "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": message}],
     "temperature": 0.7
    }

    response = requests.post(endpoint, headers=headers, json=data)
    response_data = response.json()

    return response_data
#print(call_chatgpt_api("Treatment options in ectopic pregnancy"))