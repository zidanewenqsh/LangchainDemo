#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context({"input": "hi!"}, {"output": "What's up?"})
ret = memory.load_memory_variables({})
print(ret)
