from bs4 import BeautifulSoup
import numpy as np
from numpy.linalg import norm
from trafilatura import extract
from newspaper import Article
from sentence_transformers import SentenceTransformer

# -------------------------------
# 1. Topic definitions (safe)
# -------------------------------
IDEAL_TOPICS = {
    "what is": ["what is", "definition", "overview", "introduction", "explain"],
    "why matters": ["why", "importance", "benefit", "significance", "reason"],
    "how works": ["how", "process", "mechanism", "steps", "workflow"],
    "examples": ["example", "case study", "instance", "illustration"],
    "problems": ["problem", "issue", "challenge", "limitation", "risk"],
    "best practices": ["best practice", "recommendation", "guideline", "tip"]
}

# -------------------------------
# 2. Lazy globals (IMPORTANT)
# -------------------------------
_model = None
_topic_embeddings = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_topic_embeddings():
    global _topic_embeddings
    if _topic_embeddings is None:
        model = get_model()
        _topic_embeddings = {
            topic: np.mean(model.encode(keywords), axis=0)
            for topic, keywords in IDEAL_TOPICS.items()
        }
    return _topic_embeddings


# -------------------------------
# 3. Content extraction (optimized)
# -------------------------------
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

    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(" ")


# -------------------------------
# 4. Math helper
# -------------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


# -------------------------------
# 5. Semantic coverage metric
# -------------------------------
def semantic_topic_coverage(html, url=None, threshold=0.6):
    text = extract_main_content(html, url)

    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
    if not paragraphs:
        return {"topic_coverage_score": 0.0}

    model = get_model()
    topic_embeddings = get_topic_embeddings()

    para_embeddings = model.encode(
        paragraphs,
        batch_size=8,
        show_progress_bar=False
    )

    covered_topics = 0
    for topic_vec in topic_embeddings.values():
        if any(cosine_similarity(topic_vec, p_vec) >= threshold for p_vec in para_embeddings):
            covered_topics += 1

    return {
        "topic_coverage_score": covered_topics / len(topic_embeddings)
    }