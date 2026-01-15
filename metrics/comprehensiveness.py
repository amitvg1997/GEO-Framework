from bs4 import BeautifulSoup

IDEAL_TOPICS = {
    "what is": ["what is", "definition", "overview", "introduction", "explain"],
    "why matters": ["why", "importance", "benefit", "significance", "reason"],
    "how works": ["how", "process", "mechanism", "steps", "workflow"],
    "examples": ["example", "case study", "instance", "illustration"],
    "problems": ["problem", "issue", "challenge", "limitation", "risk"],
    "best practices": ["best practice", "recommendation", "guideline", "tip"]
}

def comprehensiveness_metrics(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ").lower()
    
    covered_topics = 0
    for topic, keywords in IDEAL_TOPICS.items():
        if any(keyword in text for keyword in keywords):
            covered_topics += 1
    
    topic_coverage_score = covered_topics / len(IDEAL_TOPICS)
    
    return {
        "topic_coverage_score": topic_coverage_score
    }
