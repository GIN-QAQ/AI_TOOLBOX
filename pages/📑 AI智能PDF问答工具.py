import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils4 import qa_agent

st.title("📑 AI智能PDF问答工具 ")

# 尝试从会话状态获取 OpenAI API 密钥，如果不存在则显示输入框
if 'openai_api_key' not in st.session_state:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key


# 初始化会话状态中的记忆
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
question = st.text_input("对PDF内容进行提问", disabled=not uploaded_file)

if 'openai_api_key' in st.session_state:
    if uploaded_file and question and not st.session_state['openai_api_key']:  # 优化：明确使用 st.session_state['openai_api_key']
        st.info("请输入你的OpenAI API密钥")

if uploaded_file and question and not st.session_state['openai_api_key']:  # 优化：明确使用 st.session_state['openai_api_key']
    st.info("请输入你的OpenAI API密钥")

if uploaded_file and question and st.session_state['openai_api_key']:  # 优化：明确使用 st.session_state['openai_api_key']
    with st.spinner("AI正在思考中，请稍等..."):
        try:
            response = qa_agent(st.session_state['openai_api_key'], st.session_state["memory"],
                                uploaded_file, question)
        except Exception as e:
            st.error(f"处理过程中出错: {e}")
            response = None
            if response:
                st.write("### 答案")
                st.write(response["answer"])
                st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i + 1]
            st.write(f"**你**：{human_message.content}")
            st.write(f"**AI**：{ai_message.content}")
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()
