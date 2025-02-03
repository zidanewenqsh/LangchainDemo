import os
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 加载环境变量
load_dotenv()

# 初始化 ChatOpenAI
llm = ChatOpenAI(
    model="deepseek-chat",  # 使用 DeepSeek 模型
    temperature=0.7,
    streaming=True,
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

def respond(message, chat_history):
    bot_message = chain.invoke({"input": message})
    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# AI 助手\n请输入您的问题")
    
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, None),
        height=500,
        type="messages"  # 使用新的消息格式
    )
    
    txt = gr.Textbox(
        show_label=False,
        placeholder="输入您的问题...",
        container=False
    )

    txt.submit(respond, [txt, chatbot], [txt, chatbot])
    
if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",  # 明确使用本地主机
        server_port=7860,
        share=True
    ) 