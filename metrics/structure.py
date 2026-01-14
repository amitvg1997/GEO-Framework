from bs4 import BeautifulSoup
import numpy as np

def structure_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    words = len(text.split())

    h1 = len(soup.find_all("h1"))
    h2 = len(soup.find_all("h2"))
    h3 = len(soup.find_all("h3"))
    p_lengths = [len(p.get_text().split()) for p in soup.find_all("p")]

    faq = sum(1 for p in soup.find_all("p") if p.get_text().strip().endswith("?"))

    return {
        "h1_count": h1,
        "h2_count": h2,
        "h3_count": h3,
        "headers_to_text_ratio": (h1 + h2 + h3) / max(words, 1),
        "paragraph_length_variance": np.var(p_lengths) if p_lengths else 0,
        "faq_density": faq
    }