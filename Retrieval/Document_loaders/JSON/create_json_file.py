#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Sample data as a Python dictionary
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Specify the file name
json_file = 'sample_data.json'

# Write the data to the JSON file
with open(json_file, 'w') as file:
    json.dump(data, file, indent=4)

print(f'{json_file} has been created.')
