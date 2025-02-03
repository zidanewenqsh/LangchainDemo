import os
from dotenv import load_dotenv
import gradio as gr
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
import time
import logging
import sys
import backoff
import socket
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()
logger.info("环境变量加载完成")

# 初始化 Ollama
try:
    llm = Ollama(
        model="qwen2.5:7b",
        temperature=0.7,
        base_url="http://localhost:11434",
        timeout=120
    )
    logger.info("Ollama LLM 初始化成功")
except Exception as e:
    logger.error(f"Ollama LLM 初始化失败: {str(e)}")
    raise

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI助手，请用简洁的语言回答用户的问题。"),
    ("human", "{input}")
])
logger.info("提示模板创建成功")

# 创建处理链
chain = prompt | llm | StrOutputParser()
logger.info("处理链创建成功")

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

# 修改 check_ollama_service 函数
@backoff.on_exception(backoff.expo, 
                     (requests.exceptions.RequestException, socket.error),
                     max_tries=3)
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

# 修改 respond 函数
@backoff.on_exception(backoff.expo, 
                     (requests.exceptions.RequestException, socket.error),
                     max_tries=3)
def respond(message, chat_history):
    logger.info("=== 开始新的响应处理 ===")
    logger.info(f"输入消息: {message}")
    logger.info(f"当前聊天历史长度: {len(chat_history)}")
    
    try:
        # 检查输入是否为空
        if not message or message.isspace():
            logger.warning("收到空消息")
            return "", chat_history
            
        # 检查 Ollama 服务
        if not check_ollama_service():
            error_msg = "Ollama 服务未启动或连接不稳定，请检查服务状态"
            logger.error(error_msg)
            return error_msg, chat_history
            
        # 使用 LangChain 链来处理请求
        logger.info("开始生成回复...")
        start_time = time.time()
        
        try:
            # 添加更多调试信息
            logger.debug(f"提示模板: {prompt}")
            logger.debug(f"LLM 配置: {llm}")
            
            # 使用之前定义的 chain 而不是直接调用 API
            logger.info("正在调用 LangChain 链...")
            
            # 使用 timeout 控制
            bot_message = chain.invoke(
                {"input": message},
                config={"timeout": 60}  # 设置60秒超时
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"生成回复成功! 用时: {elapsed_time:.2f}秒")
            logger.info(f"生成的回复: {bot_message}")
                
        except Exception as e:
            logger.error(f"生成回复时出错: {str(e)}", exc_info=True)
            bot_message = f"生成回复时出错: {str(e)}"
        
        # 更新聊天历史
        chat_history.append((message, bot_message))
        logger.info(f"聊天历史已更新，当前长度: {len(chat_history)}")
        logger.info("=== 响应处理完成 ===")
        return "", chat_history
        
    except Exception as e:
        logger.error(f"响应处理过程中发生错误: {str(e)}", exc_info=True)
        return f"发生错误: {str(e)}", chat_history

with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# DeepSeek AI 助手\n请输入您的问题")
    
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, None),
        height=500,
        type="messages"
    )
    
    txt = gr.Textbox(
        show_label=False,
        placeholder="输入您的问题...",
        container=False
    )

    # 添加清除按钮
    clear = gr.Button("清除对话")
    
    # 定义清除函数
    def clear_history():
        logger.info("清除聊天历史")
        return [], ""

    # 修改事件处理绑定
    txt.submit(
        fn=respond,
        inputs=[txt, chatbot],
        outputs=[txt, chatbot],
        api_name="chat"
    ).then(
        lambda: gr.update(interactive=True),
        None,
        [txt],
        queue=False
    )
    
    clear.click(
        fn=clear_history,
        inputs=[],
        outputs=[chatbot, txt],
        api_name="clear"
    )

    logger.info("Gradio UI 组件创建完成")

if __name__ == "__main__":
    logger.info("=== 应用程序启动 ===")
    
    # 检查日志文件权限
    try:
        with open('app.log', 'a') as f:
            f.write("=== 新会话开始 ===\n")
        logger.info("日志文件写入测试成功")
    except Exception as e:
        logger.error(f"日志文件写入测试失败: {str(e)}")
    
    # 检查 Ollama 服务
    if not check_ollama_service():
        logger.warning("警告: Ollama 服务未启动，请先运行 'ollama serve'")
    else:
        logger.info("Ollama 服务已启动")
    
    try:
        logger.info("正在启动 Gradio 服务器...")
        demo.queue(concurrency_count=1)  # 限制并发数为1
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=True,
            show_error=True,
            prevent_thread_lock=True  # 防止线程锁定
        )
        logger.info("Gradio 服务器启动成功")
    except Exception as e:
        logger.error(f"Gradio 服务器启动失败: {str(e)}", exc_info=True) 