import requests
import os

def text2audio(content: str) -> str:
    # 定义API端点和请求头
    url = "http://localhost:8080/tts"
    #url = "http://166.111.80.169:8080/tts"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 构建请求数据
    data = {
        "input": content,
        "model": "en-us-blizzard_lessac-medium.onnx"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, json=data, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            # 保存音频文件
            audio_data = response.content
            audio_file_path = "output.wav"  # 你可以指定文件路径和格式
            with open(audio_file_path, "wb") as audio_file:
                audio_file.write(audio_data)
            absolute_path = os.path.abspath(audio_file_path)
            print(absolute_path)
            return absolute_path
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {str(e)}")

    return None

if __name__ == "__main__":
    text2audio("Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West")
