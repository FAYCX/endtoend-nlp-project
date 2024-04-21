import streamlit as st

import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import os
import logging
import spacy
import re   #regular expression library to cleanup the text
import networkx as nx #for network analysis
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import os
from spacy import displacy
import numpy as np
from spacy import displacy
import networkx as nx
import matplotlib.pyplot as plt

#AI vision page


#@st.cache_data
def load_data():
    NER = spacy.load('en_core_web_md')
    with open('pride.txt', 'r', encoding='utf8') as rf:
        text = rf.read()

    # Extract the desired text portion
    text = text[text.find("Chapter 61")+len("Chapter 61"):text.find("End of the Project Gutenberg EBook")].strip()
    text = re.sub(r'\n {6}', ' ', text)
    text = text.replace(".", "")

    # Split the text into chapters and paragraphs
    chapters = re.split(r"Chapter \d{1,2}", text)
    paragraphs = text.split("\n")

    # Save chapters to individual files (optional step, depending on your need)
    output_dir = "Chapters"
    os.makedirs(output_dir, exist_ok=True)
    for i, chapter_text in enumerate(chapters, start=0):
        if not chapter_text.strip():
            continue
        filename = f"{output_dir}/{i}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(chapter_text.strip())

    # Return the NER model and the text for further processing
    return NER, chapters, text

# Load data and NER model
NER, chapters, text = load_data()

# Function to display NER visualization
def read_AI(NER, chapters, text):
    st.title("Read &lt;Pride and Prejudice&gt; in AI Vision")
    st.write("##### Entity Recognition through NLP")
    for _ in range(2):  # You can adjust the range for more or less space
        st.write("")  

    # Pagination
    chapter_index = st.selectbox("Select Chapter", range(1, len(chapters) + 1)) - 1
    selected_chapter = chapters[chapter_index]

    # Process the text with the NER model
    doc = NER(text[0:3000])  # Limiting to the first 2000 characters for demonstration
    #doc1 = NER(selected_chapter) 

    # Use displaCy to render the entities within the Streamlit app
    html = displacy.render(doc, style="ent")
    #html = displacy.render(doc1, style="ent")

    
    # Streamlit components to display HTML content
    st.write(html, unsafe_allow_html=True)

# Layout
read_AI(NER, chapters, text)




