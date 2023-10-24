#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import time

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
store = InMemoryStore()

underlying_embeddings = OpenAIEmbeddings()
embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)
t1 = time.time()
embeddings = embedder.embed_documents(["hello", "goodbye"])
t2 = time.time()
print(t2 - t1)
t1 = time.time()
embeddings_from_cache = embedder.embed_documents(["hello", "goodbye"])
t2 = time.time()
print(t2 - t1)
print(embeddings == embeddings_from_cache)
