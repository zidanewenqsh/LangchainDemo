#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Custom LLM demo."""
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())
from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

class CustomLLM(LLM):
    '''
    This is a demo of the OpenAI class in langchain.llms
    这段代码是一个自定义的LLM（Language Model Manager）类，继承自LLM类。代码的功能是创建一个自定义的LLM对象，并调用该对象的_call方法来对输入的prompt字符串进行处理。
    代码的步骤如下：
    1. 定义一个CustomLLM类，继承自LLM类。
    2. 在CustomLLM类中定义一个属性n，表示处理prompt字符串时要截取的长度。
    3. 定义一个_llm_type属性，返回字符串"custom"，表示该LLM对象的类型为自定义。
    4. 定义一个_call方法，接受一个prompt字符串作为输入，并可选地接受一个stop列表和一个run_manager对象作为参数。
    5. 在_call方法中，如果stop不为None，则抛出一个ValueError异常，表示不允许使用stop参数。
    6. 返回截取了前n个字符的prompt字符串。
    7. 定义一个_identifying_params方法，返回一个字典，包含参数n和对应的值，用于标识该LLM对象。
    8. 在if __name__ == '__main__'条件下，创建一个CustomLLM对象llm，设置n为10。
    9. 调用llm对象的_call方法，传入字符串"This is a foobar thing"作为prompt参数，将返回的结果赋给ret变量。
    10. 打印ret的值。
    11. 打印llm对象的值。
    '''
    n: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return prompt[: self.n]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}

if __name__ == '__main__':
    llm = CustomLLM(n=10)
    ret = llm("This is a foobar thing")
    print(ret)
    print(llm)