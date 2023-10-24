#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:58:00 2021
unfinshed demo of UpstashRedisStore, execution in linux
https://python.langchain.com/docs/modules/data_connection/text_embedding/caching_embeddings#using-with-a-vector-store
"""

from langchain.storage import RedisStore
# For cache isolation can use a separate DB
# Or additional namepace
store = RedisStore(redis_url="redis://localhost:6379", client_kwargs={'db': 2}, namespace='embedding_caches')

underlying_embeddings = OpenAIEmbeddings()
embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)
embeddings = embedder.embed_documents(["hello", "goodbye"])
embeddings = embedder.embed_documents(["hello", "goodbye"])
print(list(store.yield_keys()))
print(list(store.client.scan_iter()))