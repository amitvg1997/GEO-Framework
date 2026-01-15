import textstat
from bs4 import BeautifulSoup
import nltk
import os

# Point NLTK to the bundled data directory
nltk_data_path = "/var/task/nltk_data"
if os.path.exists(nltk_data_path):
    nltk.data.path.insert(0, nltk_data_path)

def readability_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    return {
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "word_count": textstat.lexicon_count(text),
        "avg_sentence_length": textstat.avg_sentence_length(text)
    }
