# AXIOM: First-Principles Mathematical Engine

AXIOM is a machine learning chatbot built entirely from mathematical first principles. It rejects black-box neural networks in favor of completely transparent, classical algorithms (Naive Bayes, TF-IDF, Markov Chains). 

## Current Status: Phase V2.1 (Robust NLP Pipeline)

AXIOM is currently in its **V2.1 Phase**. This phase upgraded the zero-training pipeline to handle real conversational edge cases mathematically using TF-IDF weights and explicit stopword isolation.

### What Works (V2 Capabilities)
- **100% Transparent Math**: Every decision AXIOM makes is exposed. The router uses Naive Bayes with Laplace smoothing, and the retriever uses Term Frequency-Inverse Document Frequency (TF-IDF) Cosine Similarity.
- **Stopword & Filler Resistance**: Queries consisting entirely of stopwords (e.g., "what is it") or conversational fillers are explicitly filtered or balanced across domains, preventing hallucinated cosine matches.
- **Chit-Chat Support**: A fully isolated `chit_chat` domain natively catches greetings, identity questions, and farewells.
- **Instant Boot Time**: Because it doesn't use gradient descent, the engine initializes instantly by reading `data/memory.json` into memory and precomputing probability matrices.

### What Doesn't Work (V2 Limitations)
While the structural math is solid, the engine is currently limited by the hardcoded vocabulary in `memory.json`.
- **Abbreviation OOV**: If you say "DL", it fails to route to `modern_context` because only "deep learning" is mapped.
- **Advanced Terminology Missing**: Topics like "AUC", "ROC", and "binary cross entropy" are missing from the `classical_ml` dataset.
- **Missing Conversational Acknowledgments**: Casual conversational bridging ("i see", "you were wrong") lacks explicit intents and causes misrouting.

For a detailed breakdown of these edge cases and OOV limitations, please read [issues.md](issues.md).

## Project Structure

- `axiom/core/router.py`: The Naive Bayes domain router.
- `axiom/core/retriever.py`: The TF-IDF intent retriever.
- `axiom/core/generator.py`: The response template generator.
- `axiom/orchestrator.py`: State management and pipeline execution.
- `cli.py`: Interactive terminal testing script.
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
