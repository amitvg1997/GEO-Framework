import json
from metrics.readability import readability_metrics
from metrics.structure import structure_metrics
from metrics.eat import eat_metrics
from metrics.entities import entity_metrics
from metrics.schema import schema_metrics
from metrics.comprehensiveness import comprehensiveness_metrics
import requests

def lambda_handler(event, context):
    body = json.loads(event["body"])
    content = body.get("content")
    url = body.get("url")

    html = content
    if url:
        html = requests.get(url, timeout=10).text

    results = {}
    results.update(readability_metrics(html))
    results.update(structure_metrics(html))
    results.update(eat_metrics(html, url))
    results.update(entity_metrics(html))
    results.update(schema_metrics(html))
    results.update(comprehensiveness_metrics(html))

    results["recommendations"] = generate_recommendations(results)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(results)
    }

def generate_recommendations(m):
    rec = []
    if m["citation_count"] < 3:
        rec.append("Add citations to reputable external sources.")
    if m["h2_count"] < 3:
        rec.append("Increase use of H2 subheadings for structure.")
    if m["schema_score"] < 0.5:
        rec.append("Add or improve schema.org structured data.")
    if m["faq_density"] == 0:
        rec.append("Add explicit Q&A sections for AI retrieval.")
    return rec