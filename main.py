#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import openai
import asyncio
from Model_IO import *

# print(os.environ.get("OPENAI_API_KEY"))
openai.api_key = os.environ.get("OPENAI_API_KEY")
cmd_dict = {key: False for key in range(100)}
if __name__ == '__main__':
    print()
    index = 0
    subindex = 0
    cmd_dict[index] = True
    if cmd_dict[0]:
        llms_demo(index=subindex)
    if cmd_dict[1]:
        asyncio.run(llms_demo_async(index=subindex))

