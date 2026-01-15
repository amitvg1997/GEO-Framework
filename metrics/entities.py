import spacy
from bs4 import BeautifulSoup
import os

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

def entity_metrics(html):
    nlp_model = load_model()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    
    # Increase spaCy's max_length to allow larger texts
    # (NER still processes in ~100k char chunks internally)
    nlp_model.max_length = 2000000  # 2M characters
    
    # Process in chunks to avoid memory issues
    chunk_size = 900000  # Process 900k chars at a time (under the 1M limit)
    entities_set = set()
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            doc = nlp_model(chunk)
            entities_set.update(ent.text for ent in doc.ents)
        except Exception as e:
            # If a chunk still fails, skip it and continue
            print(f"Error processing chunk {i}: {str(e)}")
            continue
    
    return {
        "unique_entity_count": len(entities_set)
    }
