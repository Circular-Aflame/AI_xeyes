import gradio as gr
import os
import time
from chat import chat
from search import search
from stt import audio2text
from tts import text2audio

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None

def add_text(history, text):
    global messages
    history = history + [(text, None)]
    print(history)
    messages = messages + [{"role":"user","content":text}]
    return history, gr.update(value="", interactive=False)

def add_file(history, file):
    global messages
    history = history + [((file.name,), None)]
    print(file.name)
    # 语音输入：当选择文件为wav文件时执行下面操作
    if file.name.endswith(".wav"):
        text = audio2text(file.name)
        if text:
            messages = messages + [{"role":"user","content": text}]
    # 语音输入
    print(history)
    return history


def bot(history):
    global messages
    if "/audio" in history[-1][0]:
        '''query = history[-1][0].split("/audio")[1].strip()  # 提取文本内容
        if query:
            messages[-1]["content"] = query
        response = chat(messages)
        audio_text = ""
        for character in response:
            audio_text += character
            audio_text = audio_text.replace("\\n","\n")
        print(audio_text)
        audio_response = text2audio(audio_text)
        messages = messages + [{"role":"assistant","content": audio_text}]'''
        history[-1] = (history[-1][0], ('C:\\Users\\23800\\Desktop\\AI大作业\\AI_xeyes-main\\output.wav',))
        print(history)
        return history
    else:
        # 检查搜索指令
        if "/search" in history[-1][0]:
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
        return history


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
