# MaMome NLP Summarization Project 

This project is a natural language processing pipeline custom built for [MaMome](https://www.mamome.io/),a health startup that provides customized nutrition plans to pregnant women based on their microbiome data.

## Objective

The objective of this pipeline is to generate automatic, targeted summaries from .pdfs of biomedical research articles that have been automatically downloaded from ArXiv.org and PubMed. The key information that needs to be gathered are findings related to the relationships between bacteria found in the human biome, their effects on maternal/fetal health, and their associations with different dietary factors.

## Approach

1. This pipeline first takes as input academic article .pdfs from an unknown number of journal sources and uses the PDFMiner package to extract text and create .txt files for further processing. 

2. Once converted to .txt format, files are then processed using regular expressions to clean the text of unnecessary elements and break them into paragraphs.

3. After a text version of the article is broken into paragraphs, those paragraphs are then filtered using a MaMome curated list of microbiome bacteria in order to retain just those paragraphs that contain mentions of the bacteria of interest. This filtered version is then written to a new .txt file.


**TO BE CONTINUED..**
