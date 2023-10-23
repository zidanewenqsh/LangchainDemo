#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
from langchain.prompts import PromptTemplate, ChatPromptTemplate
prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}.",
)

prompt_val = prompt_template.invoke({"adjective": "funny", "content": "chickens"})
print(prompt_val)
print(prompt_val.to_string())
print(prompt_val.to_json())
print(prompt_val.to_messages())