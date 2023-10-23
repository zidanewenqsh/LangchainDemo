#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Load Feast Store
from feast import FeatureStore
# You may need to update the path depending on where you stored it
feast_repo_path = "/home/wenquanshan/my_feature_repo/feature_repo/"
store = FeatureStore(repo_path=feast_repo_path)

# Prompts
from langchain.prompts import PromptTemplate, StringPromptTemplate
template = """Given the driver's up to date stats, write them note relaying those stats to them.
If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better

Here are the drivers stats:
Conversation rate: {conv_rate}
Acceptance rate: {acc_rate}
Average Daily Trips: {avg_daily_trips}

Your response:"""
prompt = PromptTemplate.from_template(template)
print(prompt)