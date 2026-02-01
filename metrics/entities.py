from bs4 import BeautifulSoup
from trafilatura import extract
from metrics.nlp_loader import get_nlp_model

def entity_metrics(html, url=None):
    nlp_model = get_nlp_model("en_core_web_lg")  # better model

    # Extract main content
    text = extract(html, include_comments=False, include_tables=False)
    if not text:
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ")

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    entities_set = set()

    for p in paragraphs:
        try:
            doc = nlp_model(p)
            entities_set.update(ent.text.strip().lower() for ent in doc.ents)
        except Exception:
            continue

    return {
        "unique_entity_count": len(entities_set),
    }
