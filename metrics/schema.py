from bs4 import BeautifulSoup
import json

def schema_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    scripts = soup.find_all("script", type="application/ld+json")

    score = 0
    if scripts:
        try:
            data = json.loads(scripts[0].string)
            keys = ["@type", "author", "datePublished"]
            score = sum(1 for k in keys if k in data) / len(keys)
        except:
            pass

    return {
        "schema_score": score
    }