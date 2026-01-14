from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup

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

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text, IDEAL_OUTLINE])

    similarity = (tfidf * tfidf.T).A[0,1]

    return {
        "topic_coverage_score": similarity
    }