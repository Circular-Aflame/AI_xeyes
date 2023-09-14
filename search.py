import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def search(content: str):
    params = {
        "engine": "bing",
        "q": content,
        "cc": "US",
        "api_key": "32c56b4cd66a904bbf0d8c104b3be47e5549a802e3315c675e7699a4abee823b"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    
    if organic_results:  # 检查是否有搜索结果
        # 找到organic_results中第一个“snippet”不为空的元素
        for result in organic_results:
            snippet = result.get("snippet")
            if snippet:
                search_results = snippet
                break
        else:
            search_results = "No search results found."
    else:
        search_results = "No search results found."

    return f"Please answer {content} based on the search result: \n\n{search_results}"

if __name__ == "__main__":
    search_query = "Sun Wukong"  # 你要搜索的内容
    search_results = search(search_query)
    print(search_results)
