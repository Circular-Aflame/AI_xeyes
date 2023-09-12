import os
import requests
import openai

openai.api_key = "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"


def chat(messages):
    print(messages)
    # # 调用openai接口
    # response = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=messages,
    #     temperature=0.5,
    #     stream=True,
    # )

    # for chunk in response:
    #     print(chunk)

    # return response

    response = requests.post(
        "http://166.111.80.169:8080/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.5,
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
