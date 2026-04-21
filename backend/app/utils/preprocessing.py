import re

def clean_text(text: str) -> str:
    """
    Cleans text for NLP processing.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()
