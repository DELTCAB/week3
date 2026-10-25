import streamlit as st

st.title("简单AI聊天")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    
    # 固定回复（后续可替换为真实API）
    reply = f"你说了：{prompt}。这是一个测试回复。"

    # 添加AI回复
    st.session_state.messages.append({"role": "assistant", "content":reply})
    with st.chat_message("assistant"):
        st.write(reply)