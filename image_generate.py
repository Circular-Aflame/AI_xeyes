import json
import os
import requests

def image_generate(content):
    # 构建API请求的URL
    #api_url = "http://localhost:8080/v1/images/generations"
    api_url = "http://166.111.80.169:8080/v1/images/generations"
    
    # 构建请求参数，将content作为描述图片的内容传递给API
    params = {
        "prompt": content,
        "size": "256x256"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    # 发送POST请求
    try:
        response = requests.post(api_url, data=json.dumps(params), headers=headers)
        if response.status_code == 200:
            # 解析API的响应，获取生成的图片地址
            print(content)
            result = response.json()
            print(result)
            image_url =result['data'][0]['url']
            return image_url
        else:
            # 处理API请求失败的情况
            print("wrong")
            return None
    except Exception as e:
        # 处理异常情况
        print(f"Error: {e}")
        return None
