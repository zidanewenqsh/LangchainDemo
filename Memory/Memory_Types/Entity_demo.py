#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.memory import ConversationEntityMemory
from langchain.llms import OpenAI
llm = OpenAI(temperature=0)
memory = ConversationEntityMemory(llm=llm)
_input = {"input": "Deven & Sam are working on a hackathon project"}
memory.load_memory_variables(_input)
memory.save_context(
    _input,
    {"output": " That sounds like a great project! What kind of project are they working on?"}
)
print("---")

ret = memory.load_memory_variables({"input": 'who is Sam'})
print(ret)
