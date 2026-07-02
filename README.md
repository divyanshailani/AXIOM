# AXIOM: First-Principles Mathematical Engine

AXIOM is a machine learning chatbot built entirely from mathematical first principles. It rejects black-box neural networks in favor of completely transparent, classical algorithms (Naive Bayes, TF-IDF, Markov Chains). 

## Current Status: Phase V2.2 (Production NLP Robustness)

AXIOM is currently in its **V2.2 Phase**. This phase successfully patched the OOV limitations of the Naive Bayes / TF-IDF models and introduced a robust event-sourcing memory architecture.

### What Works (V2.2 Capabilities)
- **100% Transparent Math**: Every decision AXIOM makes is exposed. The router uses Naive Bayes with Laplace smoothing, and the retriever uses TF-IDF Cosine Similarity.
- **Synonym Augmentation**: Edge case vocabulary ("DL", "AUC", "SVM") is dynamically mapped to canonical forms in real-time, drastically reducing Out-of-Vocabulary (OOV) errors.
- **Confidence-Based Fallbacks**: The Orchestrator evaluates TF-IDF cosine confidence dynamically. Low confidence technical queries mathematically fallback to `chit_chat` to catch conversational fragments (e.g., "i see", "my bad").
- **Meta-Fix Memory Patching**: Live production adjustments are stored entirely in `memory_patch.json` as a transaction log, preventing accidental corruption to the foundational engine data.
- **Instant Boot Time**: Because it doesn't use gradient descent, the engine initializes instantly by executing `bootstrap.py` and precomputing probability matrices.

## Project Structure

- `axiom/core/synonyms.py`: Abbreviation & synonym mapping layer.
- `axiom/bootstrap.py`: In-memory patching and loader script.
- `axiom/core/router.py`: The Naive Bayes domain router.
- `axiom/core/retriever.py`: The TF-IDF intent retriever.
- `axiom/core/generator.py`: The response template generator.
- `axiom/orchestrator.py`: State management and pipeline execution.
- `cli.py`: Interactive terminal testing script.
- `scripts/audit_memory.py`: Diagnostic utility for memory validation.
- `test_cases.json` & `run_tests.py`: Evaluation scripts with 51 prompts to test edge cases.

## Running AXIOM

You can test the engine live in your terminal:
```bash
python cli.py
```
Or you can run the automated 51-prompt test suite:
```bash
python run_tests.py
```

## Copyright
Copyright (c) 2026 Divyansh Ailani. All Rights Reserved. This software is proprietary and strictly confidential.
