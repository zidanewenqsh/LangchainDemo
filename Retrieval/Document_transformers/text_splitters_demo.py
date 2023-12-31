#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from langchain.text_splitter import RecursiveCharacterTextSplitter
# This is a long document we can split up.
with open('state_of_the_union.txt') as f:
    state_of_the_union = f.read()
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
print(texts[1])
print(len(texts))
