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
import re

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

def render_latex(text):
    """处理文本中的 LaTeX 公式，确保正确渲染"""
    # 保护代码块中的内容
    code_blocks = {}
    code_block_count = 0
    code_pattern = re.compile(r'```.*?```', re.DOTALL)
    
    def save_code_block(match):
        nonlocal code_block_count
        placeholder = f"CODE_BLOCK_{code_block_count}"
        code_blocks[placeholder] = match.group(0)
        code_block_count += 1
        return placeholder
    
    # 暂时保存代码块
    text = code_pattern.sub(save_code_block, text)
    
    # 不需要替换数学符号，保持原始的 $ 和 $$ 符号
    # 只需要确保它们在正确的位置
    
    # 恢复代码块
    for placeholder, code_block in code_blocks.items():
        text = text.replace(placeholder, code_block)
    
    return text

def format_message(text):
    """格式化消息，处理特殊格式"""
    if not text:
        return ""
    
    # 处理 LaTeX 公式
    text = render_latex(text)
    
    # 处理代码块格式
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    
    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                formatted_lines.append('<pre><code>')
            else:
                formatted_lines.append('</code></pre>')
        else:
            if in_code_block:
                formatted_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            else:
                # 处理行内公式，将 \( \) 转换为 $ $
                line = re.sub(r'\\\\?\(', '$', line)
                line = re.sub(r'\\\\?\)', '$', line)
                # 处理行间公式，将 \[ \] 转换为 $$ $$
                line = re.sub(r'\\\\?\[', '$$', line)
                line = re.sub(r'\\\\?\]', '$$', line)
                formatted_lines.append(line)
    
    # 直接返回格式化的文本
    return '\n'.join(formatted_lines)

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

def get_available_models():
    """获取所有可用的模型列表"""
    try:
        response = session.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            logger.info(f"可用模型列表: {model_names}")
            return model_names
        return []
    except Exception as e:
        logger.error(f"获取模型列表时出错: {str(e)}")
        return []

# 加载环境变量
load_dotenv()
logger.info("环境变量加载完成")

# 页面配置
st.set_page_config(
    page_title="Ollama AI 助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 MathJax（只在首次加载时）
if "mathjax_loaded" not in st.session_state:
    st.session_state.mathjax_loaded = True
    st.markdown("""
    <script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
            processEscapes: true,
            processEnvironments: true,
            packages: ['base', 'ams', 'noerrors', 'noundefined']
        },
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
            ignoreHtmlClass: 'tex2jax_ignore',
            processHtmlClass: 'tex2jax_process'
        },
        loader: {
            load: ['[tex]/noerrors', '[tex]/noundefined']
        },
        startup: {
            typeset: true
        }
    };
    </script>
    <script type="text/javascript" id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    """, unsafe_allow_html=True)

# 添加 CSS 样式
st.markdown("""
<style>
    .math-content {
        font-size: 1em;
        line-height: 1.6;
    }
    .math-content p {
        margin: 1em 0;
    }
    .MathJax {
        font-size: 1.1em !important;
    }
    mjx-container {
        overflow-x: auto;
        overflow-y: hidden;
        padding: 0.5em 0;
    }
    mjx-container[jax="CHTML"][display="true"] {
        margin: 1em 0;
        text-align: center;
    }
    pre code {
        display: block;
        padding: 1em;
        background-color: #f6f8fa;
        border-radius: 4px;
        overflow-x: auto;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

st.title("Ollama AI 助手")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info("初始化会话状态")

# 修改初始化部分
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# 在侧边栏添加模型选择
with st.sidebar:
    st.subheader("系统状态")
    if check_ollama_service():
        st.success("Ollama 服务运行正常")
        # 获取并显示可用模型列表
        available_models = get_available_models()
        if available_models:
            selected_model = st.selectbox(
                "选择模型",
                available_models,
                index=None,
                placeholder="请选择一个模型"
            )
            if selected_model != st.session_state.selected_model:
                st.session_state.selected_model = selected_model
                st.session_state.messages = []  # 清除历史消息
                st.rerun()
        else:
            st.error("未找到可用模型，请先安装模型")
            st.stop()
    else:
        st.error("Ollama 服务未运行")

    # 添加清除按钮
    if st.button("清除对话历史"):
        st.session_state.messages = []
        logger.info("对话历史已清除")
        st.rerun()

    # 添加调试信息显示
    if st.checkbox("显示调试信息"):
        st.subheader("调试信息")
        st.write("当前模型:", st.session_state.selected_model)
        st.write("会话消息数:", len(st.session_state.messages))
        
        if st.button("检查服务状态"):
            if check_ollama_service():
                st.success("服务正常")
            else:
                st.error("服务异常")

    # 添加 LaTeX 支持说明
    with st.expander("数学公式支持说明"):
        st.markdown("""
        本助手支持数学公式渲染：
        
        1. 行内公式：使用单个 `$` 符号
           例如：$E=mc^2$
        
        2. 公式块：使用两个 `$$` 符号
           例如：
           $$
           F = ma
           $$
           
        3. 复杂公式：
           $$
           \oint_{\partial \Omega} \mathbf{E} \cdot d\mathbf{S} = \frac{1}{\epsilon_0} \int_{\Omega} \rho dV
           $$
        """)

# 修改聊天历史显示部分
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        formatted_content = format_message(message["content"])
        st.markdown(formatted_content, unsafe_allow_html=True)

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
            
            with st.status("正在生成回复...", expanded=True) as status:
                st.write("正在处理您的问题...")
                logger.info("开始生成回复...")
                
                try:
                    if not st.session_state.selected_model:
                        st.info("请在侧边栏选择一个模型")
                        st.stop()
                        
                    # 初始化 LLM 和提示模板
                    llm = Ollama(
                        model=st.session_state.selected_model,
                        temperature=0.7,
                        base_url="http://localhost:11434",
                        timeout=120
                    )
                    
                    # 创建提示模板
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", """你是一个友好的AI助手，擅长用简洁的语言回答用户的问题。
                        - 使用 Markdown 格式来组织你的回答
                        - 对于数学公式：
                          * 行内公式使用 $ 符号，如 $E=mc^2$
                          * 独立公式块使用 $$ 符号，如：
                            $$
                            F = ma
                            $$
                        - 重要内容使用 **加粗** 或 *斜体*
                        - 使用列表和表格来组织信息
                        - 代码片段使用代码块格式
                        """),
                        ("human", "{input}")
                    ])
                    
                    # 创建处理链
                    chain = prompt | llm | StrOutputParser()
                    
                    # 使用实际的用户输入生成回复
                    response = chain.invoke({"input": user_input})
                    
                    # 模拟打字机效果
                    full_response = ""
                    for char in response:
                        full_response += char
                        formatted_response = format_message(full_response)
                        message_placeholder.markdown(
                            formatted_response,
                            unsafe_allow_html=True
                        )
                        time.sleep(0.01)
                    
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
            
            if st.button("重试"):
                st.rerun()

# 添加页脚，包含 LaTeX 示例
st.markdown("---")
st.markdown("""
powered by Ollama & LangChain 🚀

示例问题：
1. 请解释一下质能方程 $E=mc^2$
2. 写出牛顿第二定律的数学表达式
3. 计算圆的面积公式推导
4. 解释麦克斯韦方程组
""") 