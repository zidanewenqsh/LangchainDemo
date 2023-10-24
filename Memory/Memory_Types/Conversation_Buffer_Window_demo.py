#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=1)
memory.save_context({"input": "hi!"}, {"output": "What's up?"})
memory.save_context({"input": "not much you"}, {"output": "not much"})
ret = memory.load_memory_variables({})
print(ret)
