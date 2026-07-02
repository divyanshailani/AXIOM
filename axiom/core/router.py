# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import json
import numpy as np
from pathlib import Path
import re
from typing import Dict

class NaiveBayesRouter:
    def __init__(self, memory_data: dict, config_path: Path):
        self.memory = memory_data
        with open(config_path) as f:
            self.config = json.load(f)
            
        self.alpha = self.config.get('smoothing_alpha', 1.0)
        self.stopwords = set(self.config.get('stopwords', []))
        self.min_len = self.config.get('min_word_length', 2)
        
        # P(C)
        self.log_priors = {}
        for d, p in self.config.get('domain_priors', {}).items():
            self.log_priors[d] = np.log(p)
            
        self.vocab = set()
        self.word_counts = {} # domain -> word -> count
        self.total_words_per_domain = {}
        self.domains = list(self.memory['domains'].keys())
        
        self._fit()
        
    def _tokenize(self, text: str) -> list:
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if len(w) >= self.min_len and w not in self.stopwords]

    def _fit(self):
        for domain, content in self.memory['domains'].items():
            self.word_counts[domain] = {}
            self.total_words_per_domain[domain] = 0
            
            # Train on explicit router keywords
            keywords = content.get('router_keywords', [])
            for kw in keywords:
                for w in self._tokenize(kw):
                    if w not in self.stopwords:
                        self.vocab.add(w)
                        self.word_counts[domain][w] = self.word_counts[domain].get(w, 0) + 1
                        self.total_words_per_domain[domain] += 1
                        
            # Train on all questions in intents for richer vocabulary
            for intent in content.get('intents', []):
                for q in intent.get('questions', []):
                    for w in self._tokenize(q):
                        if w not in self.stopwords:
                            self.vocab.add(w)
                            self.word_counts[domain][w] = self.word_counts[domain].get(w, 0) + 1
                            self.total_words_per_domain[domain] += 1
            
        self.V = len(self.vocab)
        
        # Precompute log(P(w|c)) for all words in vocab
        self.log_likelihoods = {} # domain -> word -> logprob
        for domain in self.domains:
            self.log_likelihoods[domain] = {}
            denom = self.total_words_per_domain[domain] + self.alpha * self.V
            for w in self.vocab:
                count = self.word_counts[domain].get(w, 0)
                prob = (count + self.alpha) / denom
                self.log_likelihoods[domain][w] = np.log(prob)

    def predict_proba(self, query: str) -> Dict[str, float]:
        tokens = self._tokenize(query)
        
        log_probs = []
        for domain in self.domains:
            lp = self.log_priors.get(domain, np.log(1.0 / len(self.domains)))
            for w in tokens:
                if w in self.vocab:
                    lp += self.log_likelihoods[domain][w]
                # OOV words are ignored in standard Naive Bayes to prevent 
                # penalizing domains with larger vocabularies.
            log_probs.append(lp)
            
        # Softmax for probabilities
        log_probs = np.array(log_probs)
        # Shift for numerical stability
        shifted_log_probs = log_probs - np.max(log_probs)
        exp_probs = np.exp(shifted_log_probs)
        probs = exp_probs / np.sum(exp_probs)
        
        return {d: float(p) for d, p in zip(self.domains, probs)}
