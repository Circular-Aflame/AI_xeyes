import os
import requests


def chat(messages):
    print(messages)
    response = requests.post(
        "http://166.111.80.169:8080/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7
        }
    )
    
    if response.status_code == 200:
        try:
            data = response.json()
            assistant_response = data["choices"][0]["message"]["content"]
            return assistant_response
        except Exception as e:
            print("Error parsing JSON response:", e)
    else:
        print("API request failed with status code:", response.status_code)
    
    return "An error occurred"
