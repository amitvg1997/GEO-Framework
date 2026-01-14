import textstat
from bs4 import BeautifulSoup

def readability_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")

    return {
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "word_count": textstat.lexicon_count(text),
        "avg_sentence_length": textstat.avg_sentence_length(text)
    }