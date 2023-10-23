#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain.document_loaders import TextLoader

loader = TextLoader("./index.md")
ret = loader.load()
print(ret)
print(ret[0].page_content)