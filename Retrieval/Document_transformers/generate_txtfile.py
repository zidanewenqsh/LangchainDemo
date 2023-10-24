#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample content for the State of the Union address
content = """State of the Union Address
Date: January 30, 2023

My fellow Americans,

Tonight, I stand before you to report on the state of our great nation. We have faced numerous challenges, but we have also seen incredible resilience and unity among our people.

Our economy is strong, and we are making strides in healthcare, education, and infrastructure. We must continue to work together to build a brighter future for all.

Thank you, and God bless America.
"""

# Create and write to the file
with open("state_of_the_union.txt", "w") as file:
    file.write(content)

print("The text file 'state_of_the_union.txt' has been generated.")
