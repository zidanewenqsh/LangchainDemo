#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import os
# import platform
# from dotenv import load_dotenv
# envfile = ""
# if platform.system() == "Windows":
#     envfile = "D:/MyProjects/LangchainDemo/.env"
# elif platform.system() == "Linux":
#     envfile = "/data/home/wenquanshan/MyProjects/LangchainDemo/.env"
# assert len(envfile) > 0
# _ = load_dotenv(envfile)

from langchain.memory import ConversationBufferMemory

from langchain.llms import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(),
)
ret = conversation.predict(input="Hi, there!")
print(ret)
ret = conversation.predict(input="Tell me about yourself.")
print(ret)