import textstat
from bs4 import BeautifulSoup
from trafilatura import extract

def readability_metrics(html, url=None):
    # Extract main content
    text = extract(html, include_comments=False, include_tables=False)
    if not text:
        # fallback to full page
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ")

    return {
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "word_count": textstat.lexicon_count(text),
        "avg_sentence_length": textstat.avg_sentence_length(text)
    }
