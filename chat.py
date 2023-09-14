import os
import requests

# import openai
# openai.api_key = "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"


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
        # "http://localhost:8080/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.5,
        },
        stream=True,  # 使用流式请求
    )

    if response.status_code == 200:
        try:
            started = False  # 标志是否开始传输
            buffer = ""  # 用于缓存 JSON 响应的内容
            transmitted = False  # 标志是否成功传输响应内容
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    chunk_str = chunk.decode('utf-8')
                    buffer += chunk_str
                    if chunk_str == '"' and buffer[-2] !="\\":
                        if buffer.endswith('"content":"'):
                            started = True
                            chunk_str=""
                        elif started:
                            started = False  # 标记为停止传输
                            transmitted = True  # 表示成功传输了响应内容
                    if started:
                        yield chunk_str
            if transmitted:
                return  # 如果成功传输响应内容，不返回错误信息
        except Exception as e:
            print("Error parsing JSON response:", e)
    else:
        print("API request failed with status code:", response.status_code)

    yield "An error occurred"  # 在最后返回错误消息
