from bs4 import BeautifulSoup
from metrics.nlp_loader import get_nlp_model

def entity_metrics(html):
    nlp_model = get_nlp_model("en_core_web_sm")
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    
    nlp_model.max_length = 2000000
    
    chunk_size = 900000
    entities_set = set()
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            doc = nlp_model(chunk)
            entities_set.update(ent.text for ent in doc.ents)
        except Exception as e:
            print(f"Error processing chunk {i}: {str(e)}")
            continue
    
    return {
        "unique_entity_count": len(entities_set)
    }
