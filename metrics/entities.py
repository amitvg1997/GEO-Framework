import spacy
from bs4 import BeautifulSoup
import os

# Lazy load the model only when needed
nlp = None

def load_model():
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not found, download it
            os.system("python -m spacy download en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    return nlp

def entity_metrics(html):
    nlp_model = load_model()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    doc = nlp_model(text)
    entities = set(ent.text for ent in doc.ents)
    return {
        "unique_entity_count": len(entities)
    }
