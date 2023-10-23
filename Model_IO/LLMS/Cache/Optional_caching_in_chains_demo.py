#!/bin/bash
# -*- coding: utf-8 -*-

"""
"""
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

from langchain.llms import OpenAI
llm = OpenAI(model_name="text-davinci-002")
no_cache_llm = OpenAI(model_name="text-davinci-002", cache=False)
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain

text_splitter = CharacterTextSplitter()
with open('state_of_the_union.txt') as f:
    state_of_the_union = f.read()
texts = text_splitter.split_text(state_of_the_union)
from langchain.docstore.document import Document
docs = [Document(page_content=t) for t in texts[:3]]
from langchain.chains.summarize import load_summarize_chain
chain = load_summarize_chain(llm, chain_type="map_reduce", reduce_llm=no_cache_llm)
ret = chain.run(docs)
print(ret)