#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
from langchain.llms import OpenAI
from langchain.llms.loading import load_llm
llm = load_llm("llm.json")
llm.save("llm.yaml")
print(llm("Hello"))
