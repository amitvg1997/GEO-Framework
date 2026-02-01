import re
from bs4 import BeautifulSoup
from trafilatura import extract
from newspaper import Article


def extract_main_content(html, url=None):
    """
    Try trafilatura first, fall back to newspaper3k.
    Returns (text, html_fragment_used)
    """

    # 1️⃣ Try trafilatura
    text = extract(html, include_comments=False, include_tables=False)
    if text:
        return text, None

    # 2️⃣ Fallback to newspaper3k (needs URL)
    if not url:
        return None, None

    article = Article(url)
    article.set_html(html)
    article.parse()

    if article.text:
        return article.text, article.html

    return None, None


def eat_metrics(html, url=None):
    text, extracted_html = extract_main_content(html, url)

    if not text:
        return {
            "citation_count": 0,
            "author_present": False,
            "date_present": False,
            "https": url.startswith("https") if url else True
        }

    # --- AUTHOR ---
    author_present = bool(re.search(r"\bauthor\b|\bby\s+[A-Z]", text, re.I))

    # --- DATE ---
    date_present = bool(re.search(r"\b(19|20)\d{2}\b", text))

    # --- CITATIONS ---
    citation_count = 0
    if extracted_html:
        soup = BeautifulSoup(extracted_html, "lxml")
        citation_count = len([
            a for a in soup.find_all("a", href=True)
            if a["href"].startswith("http")
        ])

    return {
        "citation_count": citation_count,
        "author_present": author_present,
        "date_present": date_present,
        "https": url.startswith("https") if url else True
    }
