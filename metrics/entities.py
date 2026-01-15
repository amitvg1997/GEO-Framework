from bs4 import BeautifulSoup
from metrics.nlp_loader import get_nlp_model

def entity_metrics(html):
    nlp_model = get_nlp_model("en_core_web_sm")
    soup = BeautifulSoup(html, "lxml")
    
    # Don't extract ALL text at once—process paragraphs incrementally
    entities_set = set()
    nlp_model.max_length = 2000000
    
    chunk_size = 500000  # Smaller chunks
    current_chunk = ""
    
    # Extract text from paragraphs only (reduces memory)
    for p in soup.find_all("p"):
        text = p.get_text(" ")
        current_chunk += text + " "
        
        # Process chunk when it reaches size limit
        if len(current_chunk) > chunk_size:
            try:
                doc = nlp_model(current_chunk)
                entities_set.update(ent.text for ent in doc.ents)
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
            current_chunk = ""  # Clear memory
    
    # Process remaining text
    if current_chunk:
        try:
            doc = nlp_model(current_chunk)
            entities_set.update(ent.text for ent in doc.ents)
        except Exception as e:
            print(f"Error processing final chunk: {str(e)}")
    
    return {
        "unique_entity_count": len(entities_set)
    }
