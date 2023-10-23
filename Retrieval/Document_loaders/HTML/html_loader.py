#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
need nltk_data
"""

from langchain.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader("./index.html")
data = loader.load()
print(data)
# [Document(page_content='hello world', metadata={'source': './index.html'})]

# Loading HTML with BeautifulSoup4
from langchain.document_loaders import BSHTMLLoader
loader = BSHTMLLoader("./index.html")
data = loader.load()
print(data)
# [Document(page_content='\n\n\nTitle\n\n\nhello world\n\n', metadata={'source': './index.html', 'title': 'Title'})]
