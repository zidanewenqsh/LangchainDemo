#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
_ = load_dotenv("/data/home/wenquanshan/MyProjects/LangchainDemo/.env")
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