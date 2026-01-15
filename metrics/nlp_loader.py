import spacy
import os

# Single global instance, loaded once
_nlp_model = None

def get_nlp_model(model_name="en_core_web_sm"):
    """Load spaCy model once and reuse across all metrics."""
    global _nlp_model
    
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load(model_name)
        except OSError:
            os.system(f"python -m spacy download {model_name}")
            _nlp_model = spacy.load(model_name)
    
    return _nlp_model
