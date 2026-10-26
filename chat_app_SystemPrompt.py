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

# 接收用户输入
if prompt := st.chat_input("说点什么..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 调用 Groq API（带系统提示词 + 多轮对话）
    try:
        client = Groq(api_key=os.getenv("API_KEY"))
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + st.session_state.messages

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"出错了：{e}"
    
    # 添加 AI 回复
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)