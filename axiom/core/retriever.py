import json
import numpy as np
from pathlib import Path
import re
from typing import Tuple

class IntentRetriever:
    def __init__(self, memory_path: Path, config_path: Path, domain: str):
        with open(memory_path) as f:
            self.memory = json.load(f)
        with open(config_path) as f:
            self.config = json.load(f)
            
        self.domain = domain
        self.threshold = self.config.get('similarity_threshold', 0.25)
        self.fallback = self.config.get('fallback_intent', 'unknown')
        
        self.intents = self.memory['domains'].get(domain, {}).get('intents', [])
        
    def _tokenize(self, text: str) -> set:
        words = re.findall(r'\b\w+\b', text.lower())
        return set(words)
        
    def find_intent(self, query: str) -> Tuple[str, float]:
        query_set = self._tokenize(query)
        if not query_set:
            return self.fallback, 0.0
            
        best_intent = self.fallback
        best_score = 0.0
        
        for intent_obj in self.intents:
            intent_id = intent_obj['intent_id']
            max_q_score = 0.0
            for q in intent_obj.get('questions', []):
                q_set = self._tokenize(q)
                if not q_set:
                    continue
                
                # Binary BoW Cosine Similarity is equivalent to:
                # |A intersection B| / (sqrt(|A|) * sqrt(|B|))
                intersection = len(query_set.intersection(q_set))
                score = intersection / (np.sqrt(len(query_set)) * np.sqrt(len(q_set)))
                if score > max_q_score:
                    max_q_score = score
                    
            if max_q_score > best_score:
                best_score = max_q_score
                best_intent = intent_id
                
        if best_score < self.threshold:
            return self.fallback, float(best_score)
            
        return best_intent, float(best_score)
