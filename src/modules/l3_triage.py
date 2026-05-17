import re

# Common words to ignore so we don't flag "Dashboard" or "Processing"
STOP_WORDS = {"The", "Dashboard", "Processing", "Assistant", "Input", "Status", "System"}

def gap_check(user_input, context_data):
    # Find multi-word Proper Nouns or single capitalized words
    candidates = set(re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', user_input))
    
    # Filter out common dashboard terms
    technical_terms = {t for t in candidates if t not in STOP_WORDS}
    
    missing = [t for t in technical_terms if t not in context_data]
    
    score = 1.0 if not technical_terms else (len(technical_terms) - len(missing)) / len(technical_terms)
    
    return {
        "score": round(score, 2),
        "missing": missing,
        "status": "GREEN" if score > 0.8 else "YELLOW" if score > 0.4 else "RED"
    }