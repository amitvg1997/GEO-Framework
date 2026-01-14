from bs4 import BeautifulSoup
import spacy
import os

IDEAL_OUTLINE = """
what is
why it matters
how it works
examples
common problems
best practices
"""

# Lazy load
nlp = None

def load_model():
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            os.system("python -m spacy download en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    return nlp

def comprehensiveness_metrics(html):
    nlp_model = load_model()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")

    doc_text = nlp_model(text)
    doc_outline = nlp_model(IDEAL_OUTLINE)

    similarity = doc_text.similarity(doc_outline)

    return {
        "topic_coverage_score": similarity
    }
