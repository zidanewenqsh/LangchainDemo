#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set font
pdf.set_font("Arial", size=12)

# Add a cell
pdf.cell(200, 10, txt="LangChain: A Framework for Language Model-Driven Applications", ln=True, align='C')

# Line break
pdf.ln(10)

# Inserting the content
content = """
## Introduction

LangChain is a framework designed for developing applications driven by language models. 
It offers features like Context-Awareness and Inference Capabilities.

## Key Offerings

### Components

LangChain offers abstractions for interacting with language models and a range of implementations 
for each abstraction. These components are modular and easy to use.

### Ready-Made Chains

Structured combinations of components for accomplishing specific high-level tasks are available.

## Modules

LangChain provides standard, extensible interfaces and external integrations for various modules 
like Model I/O, Retrieval, Chains, Agents, Memory, and Callbacks.

## Additional Resources

LangChain also has a rich set of community resources, including YouTube tutorials and an excellent 
list of LangChain projects compiled by KyroLabs.

## Further Reading

1. How does LangChain simplify interactions with language models?
2. How do ready-made chains help developers get started quickly?
3. How does LangChain's modular design promote scalability in applications?
"""

# Add content to PDF
pdf.multi_cell(0, 10, txt=content)

# Save the PDF with name .pdf
pdf.output("LangChain_Info.pdf")

print("PDF has been generated and saved as 'LangChain_Info.pdf'")
