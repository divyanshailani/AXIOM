# AXIOM: First-Principles Mathematical Engine

AXIOM is a machine learning chatbot built entirely from mathematical first principles. It rejects black-box neural networks in favor of completely transparent, classical algorithms (Naive Bayes, Bag-of-Words, Markov Chains). 

## Current Status: Phase V1 (Zero-Training Architecture)

AXIOM is currently in its **V1 Phase**. This phase successfully demonstrates a functioning, lightning-fast "zero-training" pipeline that operates entirely on mathematical probabilities at import time. 

### What Works (V1 Capabilities)
- **100% Transparent Math**: Every decision AXIOM makes is exposed. The router uses Naive Bayes with Laplace smoothing, and the retriever uses a Binary Bag-of-Words (Jaccard-like Cosine Similarity) approach.
- **Instant Boot Time**: Because it doesn't use gradient descent or neural network training, the engine initializes instantly by reading `data/memory.json` into memory and precomputing probability matrices.
- **Strict Fallbacks**: If a query's cosine similarity drops below 0.25, the engine refuses to hallucinate and correctly triggers an `unknown` intent fallback.

### What Doesn't Work (V1 Limitations)
Because V1 relies entirely on explicit math and exact lexical matching, it lacks semantic "understanding." 
- **No Chit-Chat**: The engine currently has no domain for general greetings or small talk. It will attempt to route greetings to a technical domain or return an unknown intent.
- **Brittle Vocabulary**: It does not understand synonyms. If you say "maths", it fails to route to classical ML because "maths" is not in the hardcoded vocabulary. It requires exact word matches.
- **Bag-of-Words Overlaps**: Queries sharing common words (like "learning") can sometimes misroute because Bag-of-Words gives equal weight to all terms.

For a detailed breakdown of these limitations and our plan to fix them using TF-IDF and GloVe embeddings in Phase V2, please read [issues.md](issues.md).

## Project Structure

- `axiom/core/router.py`: The Naive Bayes domain router.
- `axiom/core/retriever.py`: The Binary Bag-of-Words intent retriever.
- `axiom/core/generator.py`: The response template generator.
- `axiom/orchestrator.py`: State management and pipeline execution.
- `cli.py`: Interactive terminal testing script.
- `test_cases.json` & `run_tests.py`: Evaluation scripts with 50 prompts to test edge cases.

## Running AXIOM

You can test the engine live in your terminal:
```bash
python cli.py
```
Or you can run the automated 50-prompt test suite:
```bash
python run_tests.py
```
