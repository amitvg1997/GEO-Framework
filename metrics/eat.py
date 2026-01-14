from bs4 import BeautifulSoup
import re

def eat_metrics(html, url=None):
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a", href=True)

    author = bool(re.search(r"author|by\s", soup.get_text(), re.I))
    date = bool(re.search(r"\d{4}", soup.get_text()))

    return {
        "citation_count": len([l for l in links if "http" in l["href"]]),
        "author_present": author,
        "date_present": date,
        "https": url.startswith("https") if url else True
    }