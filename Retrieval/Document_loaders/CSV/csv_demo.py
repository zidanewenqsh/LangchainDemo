#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders.csv_loader import CSVLoader
loader = CSVLoader("./data.csv")
ret = loader.load()
print(ret)
for x in ret:
    print(x.page_content)