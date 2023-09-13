import requests
import os

def audio2text(file):
    # 获取文件路径
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file)
    print(file_path)

    if file.endswith(".wav"):
        url = "http://166.111.80.169:8080/v1/audio/transcriptions"
        
        # 删除显式的 "Content-Type" 头部
        headers = {}
        
        # 确保参数格式正确
        files = {
            "file": (file, open(file_path, "rb")),  # 使用元组指定文件名和文件内容
            "model": ("", "whisper-1")  # 正确指定模型参数
        }
        
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            transcription = response.json()
            print(transcription)
            return transcription
        else: 
            print("API请求返回状态码:", response.status_code)
            print("响应内容:", response.content.decode('utf-8'))  # 为调试打印响应内容
            return None
    else:
        print("文件不以 .wav 结尾")

if __name__ == "__main__":
    audio2text('sun-wukong.wav')
