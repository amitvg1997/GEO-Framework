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
            nlp = spacy.load("en_core_web_md")
        except OSError:
            os.system("python -m spacy download en_core_web_md")
            nlp = spacy.load("en_core_web_md")
    return nlp

def comprehensiveness_metrics(html):
    nlp_model = load_model()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    
    # Increase max_length to allow larger texts
    nlp_model.max_length = 2000000
    
    # Process in chunks to avoid E088 errors on large texts
    chunk_size = 900000  # 900k chars per chunk (under 1M limit)
    similarity_scores = []
    
    doc_outline = nlp_model(IDEAL_OUTLINE)
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            doc_text = nlp_model(chunk)
            similarity_scores.append(doc_text.similarity(doc_outline))
        except Exception as e:
            print(f"Error processing comprehensiveness chunk {i}: {str(e)}")
            continue
    
    # Average similarity across chunks
    avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    return {
        "topic_coverage_score": avg_similarity
    }
