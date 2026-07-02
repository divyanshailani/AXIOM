# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
import numpy as np
from pathlib import Path
import re
from typing import Tuple

class IntentRetriever:
    def __init__(self, memory_data: dict, config_path: Path, domain: str):
        self.memory = memory_data
        with open(config_path) as f:
            self.config = json.load(f)
            
        self.domain = domain
        self.threshold = self.config.get('similarity_threshold', 0.25)
        self.fallback = self.config.get('fallback_intent', 'unknown')
        self.stopwords = set(self.config.get('stopwords', []))
        
        self.intents = self.memory['domains'].get(domain, {}).get('intents', [])
        
        # Precompute TF-IDF model for this domain
        self.vocab_idx = {}
        self.idf = np.array([])
        self.intent_vectors = []
        self._build_tfidf_model()
        
    def _tokenize(self, text: str) -> list:
        # Return list of words to preserve term frequency
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in self.stopwords]
        
    def _build_tfidf_model(self):
        if not self.intents:
            return
            
        num_docs = len(self.intents)
        vocab = set()
        intent_docs = [] # List of lists of tokens
        
        # 1. Build Vocabulary
        for intent_obj in self.intents:
            doc_tokens = []
            for q in intent_obj.get('questions', []):
                doc_tokens.extend(self._tokenize(q))
            intent_docs.append(doc_tokens)
            vocab.update(doc_tokens)
            
        vocab_list = list(vocab)
        self.vocab_idx = {w: i for i, w in enumerate(vocab_list)}
        vocab_size = len(vocab_list)
        
        if vocab_size == 0:
            return
            
        # 2. Calculate Document Frequency (DF)
        df = np.zeros(vocab_size)
        for tokens in intent_docs:
            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[self.vocab_idx[t]] += 1
                
        # 3. Calculate Inverse Document Frequency (IDF)
        # Using standard smoothed IDF: log(N / (df + 1)) + 1
        self.idf = np.log((num_docs + 1) / (df + 1)) + 1.0
        
        # 4. Precompute TF-IDF vectors for each intent
        for tokens in intent_docs:
            tf = np.zeros(vocab_size)
            for t in tokens:
                tf[self.vocab_idx[t]] += 1
                
            # L2 Normalization (Cosine Similarity preparation)
            tfidf_vec = tf * self.idf
            norm = np.linalg.norm(tfidf_vec)
            if norm > 0:
                tfidf_vec = tfidf_vec / norm
                
            self.intent_vectors.append(tfidf_vec)
            
    def _vectorize_query(self, query: str) -> np.ndarray:
        tokens = self._tokenize(query)
        vocab_size = len(self.vocab_idx)
        
        if vocab_size == 0 or not tokens:
            return np.zeros(0)
            
        tf = np.zeros(vocab_size)
        for t in tokens:
            if t in self.vocab_idx:
                tf[self.vocab_idx[t]] += 1
                
        tfidf_vec = tf * self.idf
        norm = np.linalg.norm(tfidf_vec)
        if norm > 0:
            tfidf_vec = tfidf_vec / norm
            
        return tfidf_vec

    def find_intent(self, query: str) -> Tuple[str, float]:
        if not self.intents or len(self.vocab_idx) == 0:
            return self.fallback, 0.0
            
        query_vec = self._vectorize_query(query)
        if np.linalg.norm(query_vec) == 0:
            return self.fallback, 0.0
            
        best_intent = self.fallback
        best_score = 0.0
        
        for i, doc_vec in enumerate(self.intent_vectors):
            # Dot product of two L2 normalized vectors is Cosine Similarity
            score = np.dot(query_vec, doc_vec)
            if score > best_score:
                best_score = score
                best_intent = self.intents[i]['intent_id']
                
        if best_score >= self.threshold:
            return best_intent, float(best_score)
            
        return self.fallback, float(best_score)
