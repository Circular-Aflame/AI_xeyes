import os
import re
import requests
import json

def generate_text(prompt):
    response = requests.post(
        'http://localhost:8080/v1/completions',
        json = {
            'model': 'gpt-3.5-turbo',
            'prompt': prompt,
            'temperature': 0.5,
        },
        stream=True,
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
                        if buffer.endswith('"text":"'):
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

    yield "An error occurred11"  # 在最后返回错误消息

def generate_answer(current_file_text: str, content: str):
    question = f"Please answer the question {content} according to the following content:\n\n{current_file_text}"
    return question

def generate_summary(current_file_text: str):
    content = rf"Act as a summarizer. Please summarize the following content: \n\n{current_file_text}"
    content = content.replace('\n', '\\n')
    response = requests.post(
        'http://localhost:8080/v1/chat/completions',
        json = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': content}],
            'temperature': 0.5,
        },
    )
    if response.status_code == 200:
        return json.loads(response.text)['choices'][0]['message']['content']

if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)