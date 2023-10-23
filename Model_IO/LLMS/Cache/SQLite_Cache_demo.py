#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())
from langchain.globals import set_llm_cache
from langchain.llms import OpenAI

# To make the caching really obvious, lets use a slower model.
llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)
# We can do the same thing with a SQLite cache
from langchain.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))
ret = llm.predict("Tell me a joke")
print(ret)