#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from pydantic import BaseModel
from typing import List, Dict, Any
llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm)
)
ret = conversation.predict(input="Deven & Sam are working on a hackathon project")
print(ret)
conversation.memory.entity_store.store
conversation.predict(input="They are trying to add more complex memory structures to Langchain")
conversation.predict(input="They are adding in a key-value store for entities mentioned so far in the conversation.")
conversation.predict(input="What do you know about Deven & Sam?")
