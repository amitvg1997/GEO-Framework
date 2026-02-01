from bs4 import BeautifulSoup
import numpy as np
from trafilatura import extract

def extract_main_content(html, url=None):
    """Return main article text and HTML block using trafilatura, fallback to newspaper3k"""
    text = extract(html, include_comments=False, include_tables=False)
    if text:
        return text, None  # no need for HTML parsing

    return None, None

def structure_metrics(html, url=None):
    text, extracted_html = extract_main_content(html, url)

    # fallback if extraction fails
    if not text:
        soup = BeautifulSoup(html, "lxml")
        main_soup = soup
        text = soup.get_text(" ")
    else:
        # if trafilatura returned HTML block, parse it; else use full soup for headers
        if extracted_html:
            main_soup = BeautifulSoup(extracted_html, "lxml")
        else:
            main_soup = BeautifulSoup("<div>" + text + "</div>", "lxml")

    words = len(text.split())

    h1 = len(main_soup.find_all("h1"))
    h2 = len(main_soup.find_all("h2"))
    h3 = len(main_soup.find_all("h3"))
    p_lengths = [len(p.get_text().split()) for p in main_soup.find_all("p")]

    faq = sum(1 for p in main_soup.find_all("p") if p.get_text().strip().endswith("?"))

    return {
        "h1_count": h1,
        "h2_count": h2,
        "h3_count": h3,
        "headers_to_text_ratio": (h1 + h2 + h3) / max(words, 1),
        "paragraph_length_variance": np.var(p_lengths) if p_lengths else 0,
        "faq_density": faq
    }
