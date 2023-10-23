#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from langchain.document_loaders import JSONLoader
from pathlib import Path
from pprint import pprint
data = json.loads(Path("./sample_data.json").read_text())
print(data)

loader = JSONLoader(
    file_path='./data.json',
    jq_schema='.messages[].content',
    text_content=False)

data = loader.load()

# pprint(data)

# JSON Lines file
file_path = './chat_messages.json'
pprint(Path(file_path).read_text())

loader = JSONLoader(
    file_path=file_path,
    jq_schema='.content',
    text_content=False,
    json_lines=True)

data = loader.load()
print(data)