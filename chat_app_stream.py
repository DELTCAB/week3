import streamlit as st
from groq import Groq
import os

st.title("简单AI聊天")

# 系统提示词
SYSTEM_PROMPT = "你是一个友好的助手，回答要简洁易懂。"

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏：清空按钮
with st.sidebar:
    st.header("操作")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def generate_reply(messages):
    client = Groq(api_key=os.getenv("API_KEY"))
    stream = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 接收用户输入
if prompt := st.chat_input("说点什么..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 准备消息（带系统提示词）
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + st.session_state.messages
    
    # 流式显示 AI 回复
    with st.chat_message("assistant"):
        reply = st.write_stream(generate_reply(messages))
    
    # 保存完整回复
    st.session_state.messages.append({"role": "assistant", "content": reply})