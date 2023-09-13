import os
import re
import requests

def generate_text(prompt):
    result = requests.post(
        'http://localhost:8080/v1/chat/completions',
        json = {
            'model': 'gpt-3.5-turbo',
            'prompt': prompt,
            'temperature': 0.7,
        }
    )
    return result

def generate_answer(current_file_text: str, content: str):
    """
    TODO
    """
    pass

def generate_summary(current_file_text: str):
    content = f"Act as a summarizer. Please summarize the following content:\n\n{current_file_text}"
    summary_prompt = requests.post(
        'http://localhost:8080/v1/chat/completions',
        json = {
            'model': 'gpt-3.5-turbo',
            'message': content,
            'temperature': 0.7
        }
    )
    return summary_prompt

if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)