#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}.",
)
ret = prompt_template.format(adjective="funny", content="chickens")
print(ret)

prompt_template2 = PromptTemplate(
    input_variables=["adjective", "content"],
    template="Tell me a {adjective} joke about {content}.",
)
ret = prompt_template2.format(adjective="funny", content="chickens")
print(ret)
