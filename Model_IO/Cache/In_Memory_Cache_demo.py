#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Error:
   ImportError: cannot import name 'Row' from 'sqlalchemy' (D:\MySoft\anaconda3\lib\site-packages\sqlalchemy\__init__.py)
"""
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

from langchain.globals import set_llm_cache
from langchain.llms import OpenAI

# To make the caching really obvious, lets use a slower model.
llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)

from langchain.cache import InMemoryCache
set_llm_cache(InMemoryCache())

# The first time, it is not yet in cache, so it should take longer
llm.predict("Tell me a joke")