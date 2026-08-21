# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import collections
import json
import re
from typing import Tuple

import numpy as np
from pathlib import Path


class IntentRetriever:
    """TF-IDF cosine matcher that scores a query against a domain's intents.

    The model is built at construction time from both the intent questions and
    the intent key_terms (domain vocabulary that would otherwise never enter
    the vector space, e.g. 'xgboost', 'kernel trick'). Char n-grams are added
    so short near-miss tokens ('hiii', 'knnn') still contribute noise-tolerant
    signal without touching the TF/IDF math itself.
    """

    def __init__(self, memory_data: dict, config_path: Path, domain: str):
        self.memory = memory_data
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

        self.domain = domain
        self.threshold = self.config.get('similarity_threshold', 0.15)
        self.fallback = self.config.get('fallback_intent', 'unknown')
        self.stopwords = set(self.config.get('stopwords', []))
        self.use_ngrams = self.config.get('use_char_ngrams', False)
        self.ngram_n = int(self.config.get('char_ngram_n', 3))

        self.intents = self.memory['domains'].get(domain, {}).get('intents', [])

        # Precompute TF-IDF model for this domain
        self.vocab_idx = {}
        self.idf = np.array([])
        self.intent_vectors = []
        self._build_tfidf_model()

    def _tokenize(self, text: str) -> list:
        words = re.findall(r"\b\w+\b", text.lower())
        filtered = [w for w in words if w not in self.stopwords]
        # A query like 'how are you' is 100% stopwords in some domains; keep the
        # raw words so the greeting still maps onto chit_chat's gen_greeting.
        return filtered if filtered else words

    def _ngram_features(self, tokens: list) -> dict:
        """Maps query tokens onto existing vocab words for near-miss tolerance.

        A near-miss word like 'hiii' contains the vocab word 'hi', and 'svmm'
        contains 'svm'. Two guarded rules keep this noise-tolerant without
        letting generic short words pollute:
          - vocab words >= ngram_n chars count when they appear inside the
            query token (svm in svmm, knn in knnn);
          - shorter vocab words (e.g. 'hi') only count as a prefix of the
            query token, so 'hiii' -> 'hi' works but a stray 'k' inside
            'bake' does not vote for clustering.
        Vocabulary does not grow and the TF-IDF math is untouched.
        """
        if not self.use_ngrams:
            return {}
        hits = collections.Counter()
        for tok in tokens:
            tok = tok.lower()
            if len(tok) < self.ngram_n:
                continue
            for vocab_word in self.vocab_idx:
                if len(vocab_word) >= self.ngram_n:
                    # full-word / substring overlap (svm in svmm)
                    if vocab_word in tok:
                        hits[vocab_word] += 1
                        continue
                    # shared char n-gram between query token and vocab word
                    for i in range(len(tok) - self.ngram_n + 1):
                        if tok[i:i + self.ngram_n] in vocab_word:
                            hits[vocab_word] += 1
                            break
                else:
                    # short vocab word (hi, k): only exact-ish prefix match
                    if tok.startswith(vocab_word):
                        hits[vocab_word] += 1
        return hits

    def _build_tfidf_model(self):
        if not self.intents:
            return

        num_docs = len(self.intents)
        vocab = set()
        intent_docs = []  # list of [word tokens] per intent

        # 1. Build Vocabulary
        for intent_obj in self.intents:
            doc_tokens = []
            for q in intent_obj.get('questions', []):
                doc_tokens.extend(self._tokenize(q))
            # key_terms are canonical vocabulary the intent knows about; fold
            # them into the doc so terms like 'xgboost' can actually match.
            for term in intent_obj.get('key_terms', []):
                doc_tokens.extend(self._tokenize(term))
            intent_docs.append(doc_tokens)
            vocab.update(doc_tokens)

        if not vocab:
            return

        vocab_list = sorted(vocab)
        self.vocab_idx = {w: i for i, w in enumerate(vocab_list)}
        vocab_size = len(vocab_list)

        # 2. Calculate Document Frequency (DF)
        df = np.zeros(vocab_size)
        for tokens in intent_docs:
            for t in set(tokens):
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

            # Char n-gram augmentation (kept in the same vector space,
            # scaled so word overlap dominates when it exists).
            if self.use_ngrams:
                ngram_counts = self._ngram_features(tokens)
                if ngram_counts:
                    ng_tf = np.zeros(vocab_size)
                    for vocab_word, cnt in ngram_counts.items():
                        ng_tf[self.vocab_idx[vocab_word]] += cnt
                    ng_norm = np.linalg.norm(ng_tf)
                    if ng_norm > 0:
                        tfidf_vec = tfidf_vec + 0.25 * (ng_tf / ng_norm)
                        tfidf_vec = tfidf_vec / np.linalg.norm(tfidf_vec)

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

        if self.use_ngrams:
            ngram_counts = self._ngram_features(tokens)
            if ngram_counts:
                ng_tf = np.zeros(vocab_size)
                for vocab_word, cnt in ngram_counts.items():
                    ng_tf[self.vocab_idx[vocab_word]] += cnt
                ng_norm = np.linalg.norm(ng_tf)
                if ng_norm > 0:
                    tfidf_vec = tfidf_vec + 0.25 * (ng_tf / ng_norm)
                    tfidf_vec = tfidf_vec / np.linalg.norm(tfidf_vec)

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