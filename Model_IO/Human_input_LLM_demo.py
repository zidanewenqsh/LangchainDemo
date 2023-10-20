#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最后没有出结果
"""
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

from langchain.llms.human import HumanInputLLM
from langchain.agents import load_tools
from  langchain.agents import initialize_agent
from langchain.agents import AgentType

# tools = load_tools(["wikipedia"])
tools = load_tools(["serpapi"])
llm = HumanInputLLM(
    prompt_func=lambda prompt: print(
        f"\n===PROMPT====\n{prompt}\n=====END OF PROMPT======"
    )
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

ret = agent.run("What is President of the United States?")
print(ret)
