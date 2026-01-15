import json
from metrics.readability import readability_metrics
from metrics.structure import structure_metrics
from metrics.eat import eat_metrics
from metrics.entities import entity_metrics
from metrics.schema import schema_metrics
from metrics.comprehensiveness import comprehensiveness_metrics
from metrics.nlp_loader import get_nlp_model
import requests

# Pre-load spaCy model at Lambda cold start
print("Initializing NLP model...")
get_nlp_model("en_core_web_sm")
print("NLP model loaded successfully")


def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return _cors_response(200, {"message": "OK"})

    # Parse body safely
    body = event.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {}
    elif isinstance(body, dict):
        pass
    else:
        body = {}

    content = body.get("content")
    url = body.get("url")

    html = content
    if url:
        try:
            html = requests.get(url, timeout=10).text
        except Exception as e:
            return _cors_response(
                400,
                {"error": f"Failed to fetch URL: {str(e)}"}
            )

    if not html:
        return _cors_response(
            400,
            {"error": "No content or URL provided"}
        )

    results = {}
    results.update(readability_metrics(html))
    results.update(structure_metrics(html))
    results.update(eat_metrics(html, url))
    results.update(entity_metrics(html))
    results.update(schema_metrics(html))
    results.update(comprehensiveness_metrics(html))
    results["recommendations"] = generate_recommendations(results)

    return _cors_response(200, results)


def _cors_response(status, body_dict):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(body_dict)
    }


def generate_recommendations(m):
    rec = []
    if m.get("citation_count", 0) < 3:
        rec.append("Add citations to reputable external sources.")
    if m.get("h2_count", 0) < 3:
        rec.append("Increase use of H2 subheadings for structure.")
    if m.get("schema_score", 0) < 0.5:
        rec.append("Add or improve schema.org structured data.")
    if m.get("faq_density", 0) == 0:
        rec.append("Add explicit Q&A sections for AI retrieval.")
    return rec
