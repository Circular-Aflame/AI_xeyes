import requests
import os

def audio2text(file):
    # 获得文件路径
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file)
    print(file_path)
    file_open = open(file_path, "rb")
    file_key = file_open.read()
    if file.endswith(".wav"):
        #url = "http://127.0.0.1:8080/v1/audio/transcriptions" 
        url = "http://166.111.80.169:8080/v1/audio/transcriptions"
        headers = {  
            "Content-Type": "multipart/form-data; boundary=<calculated when request is sent>",
        }
        """
        data = {
            "model": "whisper-1",
        }
        """
        files = {
            "file": file_key,
            "model": "whisper-1"
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            transcription = response.json()
            print(transcription)
            return transcription
        else: 
            print("API request failed with status code:", response.status_code)
            return None
    else:
        print("The file does not end with .wav")
if __name__ == "__main__":
    audio2text('sun-wukong.wav')
