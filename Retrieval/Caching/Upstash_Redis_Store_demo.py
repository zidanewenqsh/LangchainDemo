#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:58:00 2021
unfinshed demo of UpstashRedisStore, execution in linux
https://python.langchain.com/docs/modules/data_connection/text_embedding/caching_embeddings#using-with-a-vector-store
"""
from langchain.storage.upstash_redis import UpstashRedisStore
from upstash_redis import Redis
URL = "<UPSTASH_REDIS_REST_URL>"
TOKEN = "<UPSTASH_REDIS_REST_TOKEN>"

redis_client = Redis(url=URL, token=TOKEN)
store = UpstashRedisStore(client=redis_client, ttl=None, namespace="test-ns")

underlying_embeddings = OpenAIEmbeddings()
embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)
embeddings = embedder.embed_documents(["welcome", "goodbye"])
embeddings = embedder.embed_documents(["welcome", "goodbye"])
print(list(store.yield_keys()))
print(list(store.client.scan(0)))