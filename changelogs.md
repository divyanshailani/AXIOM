# Changelog

All notable changes to the AXIOM project will be documented in this file.

## [v1.0.0] - V1 Zero-Training Math Engines (Current)
### Added
- `NaiveBayesRouter` implemented from scratch using pure NumPy and Laplace smoothing.
- `IntentRetriever` implemented using Binary Bag-of-Words and Jaccard-like cosine similarity.
- `TemplateGenerator` implemented for strict, non-hallucinating template generation.
- `AxiomOrchestrator` to tie the routing and retrieval pipelines together.
- `cli.py` for interactive terminal testing.
- `memory.json` baseline containing 4 domains: `self`, `classical_ml`, `history`, `modern_context`.
- Comprehensive test suite (`pytest`) for Router and Retriever mathematical validation.

### Fixed
- Fixed Bag-of-Words cross-contamination by disabling conversation buffer context concatenation.
- Fixed Naive Bayes unknown word bias (OOV) by mathematically ignoring unknown words during inference, preventing small-vocabulary domains from winning by default.
- Expanded Naive Bayes training vocabulary to parse all intent questions, not just base router keywords.
