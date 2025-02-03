# LangchainDemo
My Langchain Demo Project
# Template
## openai key
```python
import os
import platform
from dotenv import load_dotenv
envfile = ""
if platform.system() == "Windows":
    envfile = "D:/MyProjects/LangchainDemo/.env"
elif platform.system() == "Linux":
    envfile = "/data/home/wenquanshan/MyProjects/LangchainDemo/.env"
assert len(envfile) > 0
_ = load_dotenv(envfile)
```

## 项目更新

### 新增功能

1. Streamlit 界面升级
   - 支持任意 Ollama 模型选择
   - 添加数学公式渲染支持
   - 改进错误处理和日志记录
   - 添加打字机效果
   - 支持会话历史管理

2. 界面组件
   - 添加模型选择下拉框
   - 添加调试信息面板
   - 添加数学公式支持说明
   - 添加服务状态检查

3. 数学公式支持
   ```latex
   # 行内公式
   $E = mc^2$
   
   # 公式块
   $$
   F = ma
   $$
   ```

4. 代码结构优化
   - 模块化的函数设计
   - 完整的错误处理
   - 详细的日志记录
   - 会话状态管理

### 使用说明

1. 启动 Ollama 服务：
   ```bash
   ollama serve
   ```

2. 运行 Streamlit 应用：
   ```bash
   streamlit run app_streamlit_allama_formula.py
   ```

3. 选择模型并开始对话
   - 在侧边栏选择可用的 Ollama 模型
   - 输入问题并等待回复
   - 支持数学公式和 Markdown 格式

### 待解决问题

1. Gradio 界面
   - 连接稳定性问题
   - 响应延迟问题
   - 格式渲染问题

### 依赖要求

```python
pip install streamlit langchain-community requests urllib3
pip install gradio  # 如果需要使用 Gradio 界面
```