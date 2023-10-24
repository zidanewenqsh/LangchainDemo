#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders import UnstructuredPDFLoader
loader = UnstructuredPDFLoader("LangChain_Info.pdf")
# data = loader.load()
# ImportError: cannot import name 'open_filename' from 'pdfminer.utils' (/home/wenquanshan/miniconda3/lib/python3.9/site-packages/pdfminer/utils.py)
# print(data)