import spacy
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

def entity_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    doc = nlp(text)

    entities = set(ent.text for ent in doc.ents)

    return {
        "unique_entity_count": len(entities)
    }