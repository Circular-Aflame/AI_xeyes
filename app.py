import gradio as gr
import os
import time
from chat import chat
from search import search
from stt import audio2text
from tts import text2audio
from fetch import fetch
from image_generate import image_generate
from mnist import image_classification
# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None
isimage =False

def add_text(history, text):
    global messages
    history = history + [(text, None)]
    messages = messages + [{"role":"user","content":text}]
    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    global messages
    global isimage
    history = history + [((file.name,), None)]
    # 语音输入：当选择文件为wav文件时执行下面操作
    if file.name.endswith(".wav"):
        text = audio2text(file.name)
        if text:
            messages = messages + [{"role":"user","content": text}]
    elif file.name.endswith(".png"):
        # 调用image_classification函数获取分类结果
        classification_result = image_classification(file)
        # 将分类结果添加到messages中
        if classification_result:
            messages = messages + [{"role":"user","content":classification_result}]
            isimage=True
    # 语音输入
    return history


def bot(history):
    global messages
    if "/audio" in history[-1][0]:
        query = history[-1][0].split("/audio")[1].strip()  # 提取文本内容
        if query:
            messages[-1]["content"] = query
        response = chat(messages)
        audio_text = ""
        for character in response:
            audio_text += character
            audio_text = audio_text.replace("\\n","\n")
        #print(audio_text)
        audio_response = text2audio(audio_text)
        messages = messages + [{"role":"assistant","content": audio_text}]
        history[-1] = (history[-1][0], (audio_response,))
        #print(history)
        yield history
    elif "/image" in history[-1][0] or isimage:
        # 提取用户发送的/image content命令中的内容
        if "/image" in history[-1][0]:
            content = history[-1][0].split("/image")[1].strip()
            if content:
                # 调用image_generate函数生成图片，并获取生成的图片URL
                image_url = image_generate(content)
                # 将生成的图片URL添加到AI助手的回复中
            messages = messages + [{"role": "assistant", "content": image_url}]
            history[-1] = (history[-1][0], (image_url,))
            yield history
        elif isimage:
            print(1)
            print(messages)
            pic_response=messages[-1]['content']
            history[-1] = (history[-1][0],(pic_response))
            yield history
    else:       
        # 网页总结指令
        if "/fetch" in history[-1][0]:
            query = history[-1][0].split("/fetch")[1].strip()
            messages[-1]["content"] = fetch(query)
            
        # 检查搜索指令
        elif "/search" in history[-1][0]:
            query = history[-1][0].split("/search")[1].strip()  # 提取搜索查询
            messages[-1]["content"] = search(query)  # 更新最后一条消息   
        history[-1][1]=""
        response = chat(messages)
        for character in response:
            history[-1][1] += character
            time.sleep(0.05)
            history[-1][1]=history[-1][1].replace("\\n","\n")
            yield history
        messages = messages + [{"role":"assistant","content":history[-1][1]}]


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
