#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# The JSON array from the previous code
json_array = [
    {
        "sender_name": "User 2",
        "timestamp_ms": 1675597571851,
        "content": "Bye!"
    },
    {
        "sender_name": "User 1",
        "timestamp_ms": 1675597435669,
        "content": "Oh no worries! Bye"
    },
    {
        "sender_name": "User 2",
        "timestamp_ms": 1675596277579,
        "content": "No Im sorry it was my mistake, the blue one is not for sale"
    }
]

# Specify the JSON file name
json_file = 'chat_messages.json'

# Write the JSON array to the JSON file
with open(json_file, 'w') as file:
    json.dump(json_array, file, indent=4)

print(f'{json_file} has been created.')

