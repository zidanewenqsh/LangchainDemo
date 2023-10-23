#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.document_loaders import TextLoader, DirectoryLoader
# blocking
# loader = DirectoryLoader("../", glob="**/*.md", show_progress=True, use_multithreading=True)

loader = DirectoryLoader('../', glob="**/*.md", loader_cls=TextLoader, show_progress=True, use_multithreading=True)
docs = loader.load()
print(docs)
print(len(docs))
for doc in docs:
    print(doc.page_content)

# Auto-detect file encodings with TextLoader
# Silent fail
loader = DirectoryLoader('../', glob="**/*.py", loader_cls=TextLoader,
                         show_progress=True, use_multithreading=True, silent_errors=True)
docs = loader.load()

print(len(docs))

# Auto detect encodings

text_loader_kwargs={'autodetect_encoding': True}
loader = DirectoryLoader("../", glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
docs = loader.load()
print(len(docs))
