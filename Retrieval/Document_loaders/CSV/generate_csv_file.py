#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

# Sample data
data = [
    ['Name', 'Age', 'Country'],
    ['Alice', 25, 'USA'],
    ['Bob', 30, 'Canada'],
    ['Carol', 35, 'UK'],
]

# Specify the file name
csv_file = 'data.csv'

# Write the data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f'{csv_file} has been created.')
