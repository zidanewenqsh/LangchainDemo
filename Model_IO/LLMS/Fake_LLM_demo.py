#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:06:06 2021
没什么用
"""
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())

from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

tools = load_tools(["python_repl"])

responses = ["Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
llm = FakeListLLM(responses=responses)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run("whats 2 + 2")

