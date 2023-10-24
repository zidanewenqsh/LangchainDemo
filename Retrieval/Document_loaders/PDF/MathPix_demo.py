#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders import MathpixPDFLoader

loader = MathpixPDFLoader("LangChain_Info.pdf")
pages = loader.load_and_split()
for page in pages:
    print(f"Page {page.page_number} content: {page.page_content}")