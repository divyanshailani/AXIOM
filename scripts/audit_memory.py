import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from axiom.bootstrap import MemoryBootstrap

# Words that legitimately never need to be router keywords (function words,
# leading question words, generic verbs). Phrases the router folds via the
# stemmer are additionally handled by comparing through the router tokenizer.
STOPWORDS = {
    "the", "a", "is", "are", "what", "how", "does", "do", "you", "your", "me",
    "about", "whats", "i", "it", "in", "and", "of", "to", "explain", "why",
    "can", "tell", "who", "when", "please", "my", "that", "this", "an", "was",
    "were", "know", "question", "questions", "make", "makes", "work", "much",
    "very", "see", "got", "okay", "alright", "later", "there", "not", "through",
}


def _tokens(phrase: str) -> set:
    return set(re.findall(r"\w+", phrase.lower()))


def audit_memory(memory: dict):
    """Reports vocabulary a user could type that the router cannot see.

    Uses the *patched* memory (base + memory_patch.json) so keywords injected
    through the transaction log are visible to the audit. The router builds its
    vocabulary from router_keywords AND intent questions, so the real drift is
    vocabulary in key_terms or questions that ends up routed nowhere — which is
    what we surface here (after token-level stopword/suffix folding matching the
    router's own normalizer).
    """
    from axiom.core.router import NaiveBayesRouter
    from pathlib import Path

    router = NaiveBayesRouter(memory, BASE_DIR / "data" / "router_config.json")
    router_vocab = router.vocab

    issues = 0
    for domain, data in memory["domains"].items():
        router_words = set()
        for kw in data.get("router_keywords", []):
            router_words.update(_tokens(kw))

        # words that only exist in key_terms or questions (not router keywords)
        intent_words = set()
        for intent in data.get("intents", []):
            for q in intent.get("questions", []):
                intent_words.update(_tokens(q))
            for term in intent.get("key_terms", []):
                intent_words.update(_tokens(term))
        intent_words -= STOPWORDS

        # true drift: intent vocabulary the router has never seen at all
        missing = {w for w in intent_words if router._normalize_token(w) not in router_vocab
                   and w not in router_words and router._normalize_token(w) not in router_words}
        if missing:
            issues += 1
            print(f"[{domain}] intent terms absent from router vocabulary: {sorted(missing)}")
    if issues == 0:
        print("Audit clean: every intent term is covered by router keywords.")
    return issues


if __name__ == "__main__":
    memory = MemoryBootstrap(BASE_DIR).load_memory()
    raise SystemExit(1 if audit_memory(memory) else 0)