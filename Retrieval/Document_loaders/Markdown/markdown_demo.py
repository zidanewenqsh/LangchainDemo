#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders import UnstructuredMarkdownLoader
markdown_path = "index.md"
loader = UnstructuredMarkdownLoader(markdown_path)
data = loader.load()
print(data)
print(len(data))
for x in data:
    print(x.page_content)

