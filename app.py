import json
from urllib.parse import parse_qs

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
    # Handle CORS preflight (for safety, though UI will use simple POST)
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    if method == "OPTIONS":
        return _cors_response(200, {"message": "OK"})

    raw_body = event.get("body") or ""
    body = {}

    # Try JSON first
    if isinstance(raw_body, str) and raw_body:
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            # Fallback: form-encoded (application/x-www-form-urlencoded)
            parsed = parse_qs(raw_body)
            body = {k: v[0] for k, v in parsed.items()}
    elif isinstance(raw_body, dict):
        body = raw_body

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

    try:
        results = {}
        results.update(readability_metrics(html))
        results.update(structure_metrics(html))
        results.update(eat_metrics(html, url))
        results.update(entity_metrics(html))
        results.update(schema_metrics(html))
        results.update(comprehensiveness_metrics(html))
        results["recommendations"] = generate_recommendations(results)

        return _cors_response(200, results)
    except Exception as e:
        print(f"ERROR processing request: {str(e)}")
        return _cors_response(500, {"error": f"Processing failed: {str(e)}"})


def _cors_response(status, body_dict):
    # Allow your S3 UI origin; adjust if your website URL changes
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://geo-framework-ui.s3-website.eu-central-1.amazonaws.com",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400"
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
