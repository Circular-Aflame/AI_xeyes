import os
import requests


def chat(messages):
    print(messages)
    response = requests.post(
        "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7
        }
    )
    # 解析API响应以获取AI助手的回复
    data = response.json()
    assistant_response = data["choices"][0]["message"]["content"]

    return assistant_response