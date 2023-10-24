#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:06:06 2021
This is a demo of the OpenAI class in langchain.llms
llm.invoke() is a blocking call that returns the result of the query
llm.stream() is a non-blocking call that returns a generator that yields the result of the query
llm.batch() is a blocking call that returns the result of the query
@param openai_api_key: The OpenAI API key
@return:

"""

import openai
import langchain
from langchain.llms import OpenAI
import asyncio
# 使用字典推导式创建字典，值初始化为 False
cmd_dict = {key: False for key in range(100)}

import os
from dotenv import load_dotenv
_ = load_dotenv("/data/home/wenquanshan/MyProjects/LangchainDemo/.env")
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")
# print(openai.api_key)
def llms_demo(index=0):
    '''
    This is a demo of the OpenAI class in langchain.llms
    llm.invoke() is a blocking call that returns the result of the query
    llm.stream() is a non-blocking call that returns a generator that yields the result of the query
    llm.batch() is a blocking call that returns the result of the query
    @param openai_api_key: The OpenAI API key
    @return:
    '''
    # llm = OpenAI(openai_api_key=openai_api_key)
    print("llms_demo")
    cmd_dict[index] = True
    llm = OpenAI()
    if cmd_dict[0]:
        ret = llm.invoke("What are some theories about the relationship between unemployment and inflation?")
        print(ret)
    if cmd_dict[1]:
        for chunk in llm.stream("What are some theories about the relationship between unemployment and inflation?"):
            print(chunk, end="", flush=True)
    if cmd_dict[2]:
        rets = llm.batch(["What are some theories about the relationship between unemployment and inflation?"])
        for ret in rets:
            print(ret)
    if cmd_dict[3]:
        # __call__: string in -> string out
        ret = llm("Tell me a joke")
        print(ret)
    if cmd_dict[4]:
        # generate: batch calls, richer outputs
        llm_result = llm.generate(["Tell me a joke", "Tell me a poem"] * 3)
        # You can also access provider specific information that is returned. This information is not standardized across providers.
        print(llm_result.llm_output)
        # {'token_usage': {'total_tokens': 298, 'completion_tokens': 274, 'prompt_tokens': 24}, 'model_name': 'text-davinci-003'}
        print(len(llm_result.generations))
        # print(llm_result)
        for generation in llm_result.generations:
            # print(dir(generation))
            print(generation[0].text)
            # print(type(generation))
            # break

async def  llms_demo_async(index=0):
    '''
    This is a demo of the OpenAI class in langchain.llms
    Error:
        Retrying langchain.llms.openai.acompletion_with_retry.<locals>._completion_with_retry in 4.0 seconds as it raised APIConnectionError: Error communicating with OpenAI.

    @param index:
    @return:
    '''
    print("llms_demo_async")
    cmd_dict[index] = True
    llm = OpenAI()
    if cmd_dict[0]:
        await llm.ainvoke("What are some theories about the relationship between unemployment and inflation?")
    if cmd_dict[1]:
        async for chunk in llm.astream(
                "What are some theories about the relationship between unemployment and inflation?"):
            print(chunk, end="", flush=True)
    if cmd_dict[2]:
        await llm.abatch(["What are some theories about the relationship between unemployment and inflation?"])
    if cmd_dict[3]:
        async for chunk in llm.astream_log(
                "What are some theories about the relationship between unemployment and inflation?"):
            print(chunk)


if __name__ == '__main__':
    llms_demo(0)

