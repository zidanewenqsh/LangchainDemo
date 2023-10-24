#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")
from langchain.embeddings import OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings()
embeddings = embeddings_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)
print(len(embeddings), len(embeddings[0]))
for i, embedding in enumerate(embeddings):
    print(f"Embeddings for document {i}: {len(embedding)}, {type(embedding)}")

embedded_query = embeddings_model.embed_query("What was the name mentioned in the conversation?")
print(len(embedded_query)) # 1536
print(embedded_query[:5])