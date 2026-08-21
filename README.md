# AXIOM: First-Principles Mathematical Engine

AXIOM is a machine learning chatbot built entirely from mathematical first principles. It rejects black-box neural networks in favor of completely transparent, classical algorithms (Naive Bayes, TF-IDF, and strict templated generation). Every decision AXIOM makes is exposed and inspectable.

## Current Status: Phase V2.3 (Hardening & NLP Coverage)

AXIOM is currently in its **V2.3 Phase**. This phase fixed the remaining Out-of-Vocabulary and routing gaps from V2.2, hardened the pipeline against malformed input, restored and substantially expanded the test suite, and made the documentation honest about how generation actually works.

### What Works (V2.3 Capabilities)
- **100% Transparent Math**: Every decision AXIOM makes is exposed. The router uses Naive Bayes with Laplace smoothing, and the retriever uses TF-IDF Cosine Similarity.
- **Synonym Augmentation**: Edge case vocabulary ("DL", "AUC", "SVM") plus casual/contraction forms ("u", "thx", "gimme", "whats") are dynamically mapped to canonical forms in real-time, drastically reducing Out-of-Vocabulary (OOV) errors.
- **Confidence-Based Fallbacks**: The Orchestrator evaluates TF-IDF cosine confidence dynamically. Low confidence technical queries mathematically fallback to `chit_chat` to catch conversational fragments (e.g., "i see", "my bad"). The fallback thresholds are read from `retriever_config.json` (single source of truth), and the reported confidence always belongs to the domain that actually answered.
- **Meta-Fix Memory Patching**: Live production adjustments are stored entirely in `memory_patch.json` as a transaction log, preventing accidental corruption to the foundational engine data. Patches are validated on load — a typo'd domain, action, or intent now fails loudly instead of silently doing nothing.
- **Strict, Non-Hallucinating Generation**: Responses come from hand-written response templates in the curated memory — there is no free-form text generation. This keeps every answer factual and inspectable (see note below on "Markov chain" claims).
- **Robust Input Handling**: Non-string input, empty prompts, and Ctrl-D all terminate gracefully. Short near-miss tokens ("hiii", "svmm") and all-stopword phrases ("how are you") are handled without crashes.
- **Instant Boot Time**: Because it doesn't use gradient descent, the engine initializes instantly by executing `bootstrap.py` and precomputing probability matrices.

### A Note on "Markov Chain" (Docs Honesty)
Earlier versions of this README and a few response templates claimed AXIOM "generates sentences word by word with a Markov chain". That was aspirational marketing: generation is actually `random.choice` over hand-written templates. We've corrected the documentation to match reality. Building a real Markov generator remains on the roadmap if you want it, but the current design deliberately favors strict, deterministic, non-hallucinating answers over fluent-but-possibly-incoherent free-form text.

## Project Structure

- `axiom/core/synonyms.py`: Abbreviation, synonym, and casual-contraction mapping layer.
- `axiom/bootstrap.py`: In-memory patching and loader script (validated patches).
- `axiom/core/router.py`: The Naive Bayes domain router (light stemmer + contraction folding).
- `axiom/core/retriever.py`: The TF-IDF intent retriever (key_terms-aware, char n-gram tolerance).
- `axiom/core/generator.py`: The strict response template picker.
- `axiom/orchestrator.py`: State management and pipeline execution (input guarding, config-driven fallbacks).
- `cli.py`: Interactive terminal testing script.
- `scripts/audit_memory.py`: Diagnostic utility for memory validation (patch-aware).
- `test_cases.json` & `run_tests.py`: Assert-based evaluation harness with 51 prompts and golden routing checks.
- `tests/`: pytest unit + integration suite (50 tests).

## Running AXIOM

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
Memory vocabulary can be audited with:
```bash
python scripts/audit_memory.py
```

## Copyright
Copyright (c) 2026 Divyansh Ailani. All Rights Reserved. This software is proprietary and strictly confidential.
