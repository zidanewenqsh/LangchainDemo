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