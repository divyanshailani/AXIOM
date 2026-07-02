import json
from pathlib import Path

def audit_memory(memory_path: str):
    with open(memory_path) as f:
        memory = json.load(f)
        
    for domain, data in memory["domains"].items():
        router_words = set(data.get("router_keywords", []))
        intent_words = set()
        
        for intent in data.get("intents", []):
            for q in intent.get("questions", []):
                intent_words.update(q.lower().split())
                
        # Simple stopword exclusion for the audit script
        stopwords = {"the", "a", "is", "what", "how", "does", "do", "you", "your", "me", "about", "whats", "i", "it", "in", "and", "of", "to"}
        intent_words = intent_words - stopwords
                
        missing = intent_words - router_words
        if missing:
            print(f"[{domain}] Missing router keywords: {missing}")

if __name__ == "__main__":
    audit_memory("data/memory.json")
