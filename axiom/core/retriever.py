# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import collections
import json
import re
from typing import Tuple

import numpy as np
from pathlib import Path

from axiom.core.negation import apply_negation_window


class IntentRetriever:
    """TF-IDF cosine matcher that scores a query against a domain's intents.

    The model is built at construction time from both the intent questions and
    the intent key_terms (domain vocabulary that would otherwise never enter
    the vector space, e.g. 'xgboost', 'kernel trick'). Query tokens that
    CONTAIN a vocabulary word ('svmm' contains 'svm', 'transformers' contains
    'transformer') are folded onto that word so short near-misses and plural
    forms contribute real evidence without touching the TF/IDF math itself.

    Deliberately NOT done: loose character-trigram coincidence matching. It was
    measured (V2.4 calibration) producing confident nonsense — queries with
    zero real word overlap ("what is the weather", "gradient descent") scored
    0.35-0.60 against unrelated intents purely via trigram collisions, higher
    than legitimate queries like "what are transformers". Coincidental n-grams
    are therefore never allowed to justify an answer.
    """

    def __init__(self, memory_data: dict, config_path: Path, domain: str):
        self.memory = memory_data
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

        self.domain = domain
        self.threshold = self.config.get('similarity_threshold', 0.15)
        # Relative gap the winner must hold over the runner-up; below this the
        # domain's intents are considered tied and the query is rejected as
        # ambiguous rather than answered with whichever came out on top.
        self.ambiguity_margin = self.config.get('ambiguity_margin', 0.10)
        self.fallback = self.config.get('fallback_intent', 'unknown')
        self.stopwords = set(self.config.get('stopwords', []))
        self.use_ngrams = self.config.get('use_char_ngrams', False)
        self.ngram_n = int(self.config.get('char_ngram_n', 3))
        self.use_negation = self.config.get('use_negation_window', False)
        self.negation_window = int(self.config.get('negation_window', 3))

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
        if not filtered:
            return words
        if self.use_negation:
            filtered = apply_negation_window(filtered, self.negation_window)
        return filtered

    def _ngram_features(self, tokens: list) -> dict:
        """Maps query/doc tokens onto existing vocab words for near-miss tolerance.

        Only high-trust containment rules are applied:
          - vocab words >= ngram_n chars count when they appear inside the
            token ('svm' in 'svmm', 'transformer' in 'transformers');
          - shorter vocab words (e.g. 'hi') only count as a prefix of the
            token, so 'hiii' -> 'hi' works but a stray 'k' inside 'bake'
            does not vote for clustering.
        Vocabulary does not grow and the TF-IDF math is untouched.
        """
        if not self.use_ngrams:
            return {}
        hits = collections.Counter()
        for tok in tokens:
            tok = tok.lower()
            # Negated tokens match on their content stem, so 'not_work' maps
            # onto both 'work' and 'not_work' vocabulary entries. The hit key
            # is always a word taken from the vocabulary itself — never a
            # newly constructed string.
            content = tok[4:] if tok.startswith("not_") else tok
            if len(content) < self.ngram_n:
                continue
            for vocab_word in self.vocab_idx:
                base = vocab_word[4:] if vocab_word.startswith("not_") else vocab_word
                if len(base) >= self.ngram_n:
                    # full-word / substring overlap (svm in svmm)
                    if base in tok or base in content:
                        hits[vocab_word] += 1
                elif tok.startswith(base):
                    # short vocab word (hi, k): only exact-ish prefix match
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

        # 4. Precompute TF-IDF vectors for each intent. The containment mapper
        # folds unstemmed variants already present in the docs ('trees' onto
        # 'tree'), which is why it runs here too.
        for tokens in intent_docs:
            tf = np.zeros(vocab_size)
            for t in tokens:
                tf[self.vocab_idx[t]] += 1

            tfidf_vec = tf * self.idf

            if self.use_ngrams:
                mapped = self._ngram_features(tokens)
                for vocab_word, cnt in mapped.items():
                    tfidf_vec[self.vocab_idx[vocab_word]] += cnt

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

        if self.use_ngrams:
            mapped = self._ngram_features(tokens)
            for vocab_word, cnt in mapped.items():
                tfidf_vec[self.vocab_idx[vocab_word]] += cnt

        norm = np.linalg.norm(tfidf_vec)
        if norm > 0:
            tfidf_vec = tfidf_vec / norm

        return tfidf_vec

    def find_intent_detailed(self, query: str) -> dict:
        """Scores the query and reports the full acceptance decision.

        Returns {'intent_id', 'score', 'runner_up_score', 'accepted', 'reason'}
        where reason is one of: 'accepted', 'below_threshold', 'ambiguous',
        'empty_query', 'no_model'. Rejected queries carry intent_id == fallback
        but keep the measured scores so misses stay diagnosable.
        """
        base = {
            "intent_id": self.fallback,
            "score": 0.0,
            "runner_up_score": 0.0,
            "accepted": False,
        }
        if not self.intents or len(self.vocab_idx) == 0:
            base["reason"] = "no_model"
            return base

        query_vec = self._vectorize_query(query)
        if query_vec.size == 0 or np.linalg.norm(query_vec) == 0:
            base["reason"] = "empty_query"
            return base

        scores = sorted(
            ((float(np.dot(query_vec, doc_vec)), i) for i, doc_vec in enumerate(self.intent_vectors)),
            key=lambda t: -t[0],
        )
        best_score = scores[0][0]
        runner_up = scores[1][0] if len(scores) > 1 else 0.0
        best_intent = self.intents[scores[0][1]]['intent_id']

        base["score"] = best_score
        base["runner_up_score"] = runner_up

        if best_score < self.threshold:
            base["reason"] = "below_threshold"
            return base

        rel_gap = (best_score - runner_up) / best_score if best_score > 0 else 0.0
        if len(scores) > 1 and rel_gap < self.ambiguity_margin:
            base["reason"] = "ambiguous"
            return base

        base["intent_id"] = best_intent
        base["accepted"] = True
        base["reason"] = "accepted"
        return base

    def find_intent(self, query: str) -> Tuple[str, float]:
        detail = self.find_intent_detailed(query)
        if detail["accepted"]:
            return detail["intent_id"], float(detail["score"])
        return self.fallback, float(detail["score"])
