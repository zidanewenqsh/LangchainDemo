#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
llm = OpenAI(temperature=0)
conversation_with_summary = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)
ret = conversation_with_summary.predict(input="Hi, what's up?")
# print(ret)
ret = conversation_with_summary.predict(input="What's their issues?")
# print(ret)
ret = conversation_with_summary.predict(input="Is it going well?")
# print(ret)
# Notice here that the first interaction does not appear.
ret = conversation_with_summary.predict(input="What's the solution?")
print(ret)
