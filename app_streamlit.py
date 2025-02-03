import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(page_title="AI 助手", page_icon="🤖")
st.title("AI 助手")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 初始化 ChatOpenAI
llm = ChatOpenAI(
    model="deepseek-chat",  # 使用 DeepSeek 模型
    temperature=0.7,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_BASE")
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI助手，请用简洁的语言回答用户的问题。"),
    ("human", "{input}")
])

# 创建处理链
chain = prompt | llm | StrOutputParser()

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入
if prompt := st.chat_input("请输入您的问题"):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 添加助手响应
    with st.chat_message("assistant"):
        response = chain.invoke({"input": prompt})
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response}) 