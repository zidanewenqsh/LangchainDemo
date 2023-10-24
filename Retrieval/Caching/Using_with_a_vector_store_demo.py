#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import platform
from dotenv import load_dotenv
envfile = ""
if platform.system() == "Windows":
    envfile = "D:/MyProjects/LangchainDemo/.env"
elif platform.system() == "Linux":
    envfile = "/data/home/wenquanshan/MyProjects/LangchainDemo/.env"
assert len(envfile) > 0
_ = load_dotenv(envfile)


from langchain.storage import InMemoryStore, LocalFileStore, RedisStore, UpstashRedisStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

underlying_embeddings = OpenAIEmbeddings()
fs = LocalFileStore("./cache/")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, fs, namespace=underlying_embeddings.model
)

print(list(fs.yield_keys()))

raw_documents = TextLoader("../state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
t1 = time.time()
db = FAISS.from_documents(documents, cached_embedder)
t2 = time.time()
print(t2 - t1)
t1 = time.time()
db2 = FAISS.from_documents(documents, cached_embedder)
t2 = time.time()
print(t2 - t1)
print(list(fs.yield_keys())[:5])
# print(db)