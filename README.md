# AXIOM: First-Principles Mathematical Engine

AXIOM is a machine learning chatbot built entirely from mathematical first principles. It rejects black-box neural networks in favor of completely transparent, classical algorithms (Naive Bayes, TF-IDF, and strict templated generation). Every decision AXIOM makes is exposed and inspectable.

## Current Status: Phase V2.4.1 (Calibration & Multi-Turn, Hardened)

AXIOM is currently in its **V2.4.1 Phase**. V2.4 made the retrieval thresholds measurement-driven instead of vibes-based, eliminated confident wrong answers caused by coincidental character n-grams, added negation awareness and context-based follow-up handling, and instrumented fallbacks with a miss log so future tuning stays data-driven. V2.4.1 fixed a measured context-retry hijack (accepted standalone matches no longer get reinterpreted through the previous topic), taught negation to see apostrophe contractions ("can't", "doesn't"), and added `scripts/compact_memory.py` to squash the patch log into `memory.json` once patches are stable.

### What Works (V2.4 Capabilities)
- **100% Transparent Math**: Every decision AXIOM makes is exposed. The router uses Naive Bayes with Laplace smoothing, and the retriever uses TF-IDF Cosine Similarity.
- **Synonym Augmentation**: Edge case vocabulary ("DL", "AUC", "SVM") plus casual/contraction forms ("u", "thx", "gimme", "whats") are dynamically mapped to canonical forms in real-time, drastically reducing Out-of-Vocabulary (OOV) errors.
- **Strict-Evidence Matching**: The retriever only trusts containment evidence ("svmm" contains "svm"). Coincidental char-trigram overlap — which measured *higher* on off-topic queries than on legitimate ones — can never justify an answer, and an ambiguity margin rejects near-tied winners honestly instead of guessing.
- **Confidence-Based Fallbacks + Context Retry**: Low-confidence queries mathematically fall back to `chit_chat`; fragments that cannot stand alone ("what about its variance?") get one guarded retry against the previous query so multi-turn follow-ups resolve. Gates keep social turns and standalone questions safe from hijacking.
- **Negation Awareness**: Negated phrases ("when does k-means NOT work") emit prefixed tokens ("not_work") in both router and retriever, staying fully classical. Apostrophe contractions ("can't", "doesn't", "won't") are folded back into single tokens before the negation window runs, so they behave identically to their spelled-out forms.
- **Miss Logging**: Every fallback appends a structured record (query, reason code, scores, router distribution) to `data/miss_log.jsonl`, making knowledge gaps measurable instead of anecdotal.
- **Meta-Fix Memory Patching**: Live production adjustments are stored in `data/memory_patch.json` as an idempotent transaction log; patches are validated on load and replays cannot duplicate data. `scripts/compact_memory.py` squashes the log into `memory.json` (dry-run first, verified round-trip, refuses on uncommitted memory changes).
- **Strict, Non-Hallucinating Generation**: Responses come from hand-written response templates in the curated memory — there is no free-form text generation (see the Markov note below).
- **Robust Input Handling**: Non-string input, empty prompts, punctuation-only input, and Ctrl-D all terminate gracefully.
- **Instant Boot Time**: Retrievers are precomputed once per domain at startup, so boot is instant and per-message latency stays flat.

### Known Limitations (documented honestly)
Single-word lexical collisions are inherent to Bag-of-Words: "who won the world cup" matches identity questions on "who". Separating these requires semantics or knowledge coverage, not tuning — the miss log surfaces them for future intents.

### A Note on "Markov Chain" (Docs Honesty)
Earlier versions of this README and a few response templates claimed AXIOM "generates sentences word by word with a Markov chain". That was aspirational marketing: generation is actually `random.choice` over hand-written templates. We've corrected the documentation to match reality. Building a real Markov generator remains on the roadmap if you want it, but the current design deliberately favors strict, deterministic, non-hallucinating answers over fluent-but-possibly-incoherent free-form text.

## Project Structure

- `axiom/core/synonyms.py`: Abbreviation, synonym, and casual-contraction mapping layer.
- `axiom/core/negation.py`: Shared negation-window helper for router and retriever.
- `axiom/bootstrap.py`: In-memory patching and loader script (validated, idempotent patches).
- `axiom/core/router.py`: The Naive Bayes domain router (light stemmer + contraction folding + negation windows).
- `axiom/core/retriever.py`: The TF-IDF intent retriever (key_terms-aware, containment-based tolerance, ambiguity margin).
- `axiom/core/generator.py`: The strict response template picker.
- `axiom/orchestrator.py`: State management and pipeline execution (input guarding, config-driven fallbacks, context retry, miss logging).
- `cli.py`: Interactive terminal testing script.
- `scripts/audit_memory.py`: Diagnostic utility for memory validation (patch-aware).
- `scripts/compact_memory.py`: Squashes the patch transaction log into `memory.json` with a verified round-trip.
- `test_cases.json` & `run_tests.py`: Assert-based evaluation harness with 51 prompts and golden routing checks.
- `tests/`: pytest unit + integration suite (79 tests).

## Running AXIOM

The project uses a local virtualenv (`.venv/`) — activate it first, or call `.venv/bin/python` directly:
```bash
source .venv/bin/activate
```
You can test the engine live in your terminal:
```bash
python cli.py
```
Or you can run the automated 51-prompt integration suite:
```bash
python run_tests.py
```
And the full unit test suite:
```bash
python -m pytest tests/ -v
```

## Copyright
Copyright (c) 2026 Divyansh Ailani. All Rights Reserved. This software is proprietary and strictly confidential.
