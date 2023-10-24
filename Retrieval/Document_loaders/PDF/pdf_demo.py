#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("LangChain_Info.pdf")
pages = loader.load_and_split()
print(pages)
for i, page in enumerate(pages):
    print(f"Page {i} content: {page.page_content}")