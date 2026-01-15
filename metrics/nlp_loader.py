import spacy
import os

_nlp_model = None

def get_nlp_model(model_name="en_core_web_sm"):
    """Load spaCy model - should already be in image."""
    global _nlp_model
    
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load(model_name)
            print(f"Loaded {model_name} successfully")
        except OSError as e:
            print(f"ERROR: Could not load {model_name}: {str(e)}")
            raise
    
    return _nlp_model
