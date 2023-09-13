import requests

def audio2text(file):
    api_url = "http://localhost:8080/v1/audio/transcriptions"
    #api_url = "http://166.111.80.169:8080/v1/chat/completions"
    headers = {}
    data = {
        "model": "whisper-1"  
    }
    files = {
        "file": ("audio_file", open(file, "rb"))
    }

    try:
        response = requests.post(api_url, headers=headers, data=data, files=files)
        response.raise_for_status()  # 检查响应状态
        result = response.json()  # 解析响应的JSON数据
        text_content = result.get("text", "")
        #print(text_content)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
if __name__ == "__main__":
    audio2text('sun-wukong.wav')
