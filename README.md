# MaMome NLP Summarization Project 

This project is a natural language processing pipeline custom built for [MaMome](https://www.mamome.io/),a health startup that provides customized nutrition plans to pregnant women based on their microbiome data.

## Objective

The objective of this pipeline is to generate automatic, targeted summaries from .pdfs of biomedical research articles that have been automatically downloaded from ArXiv.org and PubMed. The key information that needs to be gathered are findings related to the relationships between bacteria found in the human biome, their effects on maternal/fetal health, and their associations with different dietary factors.

## Approach

1. This pipeline first takes as input academic article .pdfs from an unknown number of journal sources and uses the PDFMiner package to extract text and create .txt files for further processing. 
&nbsp
&nbsp
2. Once converted to .txt format, files are then processed using regular expressions to clean the text of unnecessary elements and break them into paragraphs.

     - In the *Full Preprocessing* option, the cleaned text is written to a .txt file for subsequent summarization.

    - In the *Targeted Preprocessing* option, the paragraphs are filtered using a curated list of key terms such that only those paragraphs containing key terms are retained and written to a .txt file for subsequent summarization.
    
    &nbsp
    &nbsp

3. Using .txt files generated from either the *Full* or *Targeted* preprocessing step, [BERT Extractive Summarization](https://arxiv.org/pdf/1906.04165.pdf) is then applied to the text to generate extractive summaries of each article.

    - The *General* summary option uses Google Reseacrh's [BERT large uncased](https://github.com/google-research/bert) pre-trained model to generate the embeddings used for summarization.

    - Alternatively, the *PubMed* summary option uses Microsoft Research's [PubMedBert](https://www.microsoft.com/en-us/research/blog/domain-specific-language-model-pretraining-for-biomedical-natural-language-processing/) pre-trained model.

    - In addition to specifying pre-trained model, the user can also specify different length options: *terse* (4 sentences), *verbose* (15 sentences), and *default* (~ 1 sentence for every 3 paragraphs of text).

&nbsp
&nbsp

4. Once processed, summaries are then displayed via an interactive dashboard built using Streamlit.
