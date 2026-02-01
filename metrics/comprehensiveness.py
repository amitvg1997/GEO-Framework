from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from trafilatura import extract
from newspaper import Article
from numpy.linalg import norm

# --- Step 1: Define topics ---
IDEAL_TOPICS = {
    "what is": ["what is", "definition", "overview", "introduction", "explain"],
    "why matters": ["why", "importance", "benefit", "significance", "reason"],
    "how works": ["how", "process", "mechanism", "steps", "workflow"],
    "examples": ["example", "case study", "instance", "illustration"],
    "problems": ["problem", "issue", "challenge", "limitation", "risk"],
    "best practices": ["best practice", "recommendation", "guideline", "tip"]
}

# --- Step 2: Load embedding model ---
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast

# --- Step 3: Precompute topic embeddings ---
topic_embeddings = {}
for topic, keywords in IDEAL_TOPICS.items():
    embeddings = model.encode(keywords)
    topic_embeddings[topic] = np.mean(embeddings, axis=0)  # single vector per topic

# --- Step 4: Helper to extract main content ---
def extract_main_content(html, url=None):
    text = extract(html, include_comments=False, include_tables=False)
    if text:
        return text
    if url:
        article = Article(url)
        article.set_html(html)
        article.parse()
        if article.text:
            return article.text
    # fallback: full HTML text
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(" ")

# --- Step 5: Cosine similarity ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# --- Step 6: Semantic topic coverage metric ---
def semantic_topic_coverage(html, url=None, threshold=0.6):
    """
    Returns a topic coverage score [0,1] using embeddings.
    threshold: cosine similarity to count topic as covered
    """
    text = extract_main_content(html, url)
    
    # Split text into paragraphs
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    if not paragraphs:
        return {"topic_coverage_score": 0.0}

    # Compute embeddings for paragraphs
    para_embeddings = model.encode(paragraphs)

    # Count how many topics are semantically covered
    covered_topics = 0
    for topic, topic_vec in topic_embeddings.items():
        if any(cosine_similarity(topic_vec, para_vec) >= threshold for para_vec in para_embeddings):
            covered_topics += 1

    score = covered_topics / len(IDEAL_TOPICS)
    return {"topic_coverage_score": score}
