import requests
from bs4 import BeautifulSoup

def fetch(url: str):
    if url == "https://dev.qweather.com/en/help":
        # 发送HTTP GET请求获取页面内容
        response = requests.get(url)

        if response.status_code == 200:
            # 使用BeautifulSoup解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 使用CSS选择器选择p标签
            p_tags = soup.select("body > main > div > section > div.border-r10 > p:nth-child(3)")

            if p_tags:
                # 提取p标签内的文本信息
                processed_results = "\n".join(tag.get_text() for tag in p_tags)
                #print(processed_results)

                # 生成有效的提问
                #question = f"Act as a summarizer. Please summarize {url}. The following is the content:\n\n{processed_results}"

                return f"Act as a summarizer. Please summarize {url}. The following is the content:\n\n{processed_results}"

        # 如果页面请求失败、未找到符合选择器的p标签，或选择器无效，则返回None
        return None
    else:
        print("not the specific website")

if __name__ == "__main__":
    fetch("https://dev.qweather.com/en/help")