from bs4 import BeautifulSoup
import spacy

# Load spacy model once (at module level for Lambda efficiency)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model not in layer
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

IDEAL_OUTLINE = """
what is
why it matters
how it works
examples
common problems
best practices
"""

def comprehensiveness_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    
    # Process both texts
    doc_text = nlp(text)
    doc_outline = nlp(IDEAL_OUTLINE)
    
    # Calculate semantic similarity (0-1)
    similarity = doc_text.similarity(doc_outline)
    
    return {
        "topic_coverage_score": similarity
    }
