#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.memory import ChatMessageHistory
history = ChatMessageHistory()
history.add_message("hi!")
history.add_message("What's up?")
print(history.messages)