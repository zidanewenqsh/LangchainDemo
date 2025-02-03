import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('streamlit_app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 配置 requests 的重试策略
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

def check_ollama_service():
    """检查 Ollama 服务状态"""
    try:
        response = session.get(
            "http://localhost:11434/api/version",
            timeout=5
        )
        is_running = response.status_code == 200
        logger.info(f"Ollama 服务状态检查: {'运行中' if is_running else '未运行'}")
        return is_running
    except Exception as e:
        logger.error(f"检查 Ollama 服务时出错: {str(e)}")
        return False

def check_model_availability():
    """检查模型是否可用"""
    try:
        response = session.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            models = response.json()
            logger.info(f"可用模型列表: {models}")
            # 检查所有可能的模型名称变体
            model_names = [model['name'].lower() for model in models.get('models', [])]
            logger.info(f"检测到的模型: {model_names}")
            return any(name for name in model_names if 'qwen' in name)
        return False
    except Exception as e:
        logger.error(f"检查模型可用性时出错: {str(e)}")
        return False

def get_available_model_name():
    """获取可用的模型名称"""
    try:
        response = session.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            models = response.json().get('models', [])
            # 查找包含 qwen 的模型名称
            for model in models:
                name = model['name'].lower()
                if 'qwen' in name:
                    logger.info(f"找到匹配的模型: {model['name']}")
                    return model['name']
        logger.warning("未找到 Qwen 相关模型")
        return None
    except Exception as e:
        logger.error(f"获取模型名称时出错: {str(e)}")
        return None

# 加载环境变量
load_dotenv()
logger.info("环境变量加载完成")

# 页面配置
st.set_page_config(
    page_title="Ollama AI 助手",
    page_icon="🤖",
    layout="wide"
)
st.title("Ollama AI 助手")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info("初始化会话状态")

# 在初始化 Ollama 之前添加检查
if not check_ollama_service():
    st.error("Ollama 服务未运行，请先运行 'ollama serve' 命令启动服务")
    logger.error("Ollama 服务未运行")
    st.stop()

# 获取实际可用的模型名称
model_name = get_available_model_name()
if not model_name:
    st.error("未找到 Qwen 相关模型，请确保已安装正确的模型")
    logger.error("未找到可用的 Qwen 模型")
    st.stop()

# 初始化 Ollama
try:
    llm = Ollama(
        model=model_name,
        temperature=0.7,
        base_url="http://localhost:11434",
        timeout=120
    )
    # 测试 LLM 是否正常工作
    test_response = llm.invoke("test")
    logger.info(f"Ollama LLM 初始化成功，使用模型: {model_name}")
except Exception as e:
    logger.error(f"Ollama LLM 初始化失败: {str(e)}", exc_info=True)
    st.error(f"""
    Ollama 服务初始化失败，请检查：
    1. Ollama 服务是否正在运行 (ollama serve)
    2. {model_name} 模型是否正确安装
    3. 端口 11434 是否可访问
    
    错误信息: {str(e)}
    """)
    st.stop()

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI助手，请用简洁的语言回答用户的问题。"),
    ("human", "{input}")
])
logger.info("提示模板创建成功")

# 创建处理链
chain = prompt | llm | StrOutputParser()
logger.info("处理链创建成功")

# 添加侧边栏状态显示
with st.sidebar:
    st.subheader("系统状态")
    if check_ollama_service():
        st.success("Ollama 服务运行正常")
    else:
        st.error("Ollama 服务未运行")
    
    # 添加清除按钮
    if st.button("清除对话历史"):
        st.session_state.messages = []
        logger.info("对话历史已清除")
        st.experimental_rerun()

    # 添加调试信息显示
    if st.checkbox("显示调试信息"):
        st.subheader("调试信息")
        st.write("当前模型:", llm.model)
        st.write("服务地址:", llm.base_url)
        st.write("会话消息数:", len(st.session_state.messages))
        
        if st.button("检查服务状态"):
            if check_ollama_service():
                st.success("服务正常")
            else:
                st.error("服务异常")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入
if user_input := st.chat_input("请输入您的问题..."):
    logger.info(f"收到用户输入: {user_input}")
    
    # 检查 Ollama 服务状态
    if not check_ollama_service():
        st.error("Ollama 服务未运行，请先启动服务")
        logger.error("尝试生成回复时发现 Ollama 服务未运行")
        st.stop()
    
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 添加助手响应
    with st.chat_message("assistant"):
        try:
            message_placeholder = st.empty()
            
            # 添加状态指示器
            with st.status("正在生成回复...", expanded=True) as status:
                st.write("正在处理您的问题...")
                logger.info("开始生成回复...")
                
                try:
                    # 直接使用 invoke 而不是 stream
                    response = chain.invoke({"input": user_input})
                    
                    # 模拟打字机效果
                    full_response = ""
                    for char in response:
                        full_response += char
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.01)  # 添加小延迟以创建打字效果
                    
                    # 完成后更新显示
                    message_placeholder.markdown(response)
                    status.update(label="回复生成完成!", state="complete")
                    logger.info(f"成功生成回复: {response[:100]}...")
                    
                except Exception as e:
                    status.update(label="生成回复出错", state="error")
                    raise e
            
            # 保存到会话状态
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_msg = f"生成回复时出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            st.error(error_msg)
            
            # 添加重试按钮
            if st.button("重试"):
                st.experimental_rerun()

# 添加页脚
st.markdown("---")
st.markdown("powered by Ollama & LangChain 🚀") 