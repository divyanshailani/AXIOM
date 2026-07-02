# Changelog

All notable changes to the AXIOM project will be documented in this file.

## [v2.2.0] - V2 Meta-Fix & NLP Robustness (Current)
### Added
- **Memory Patching Workflow**: Added `axiom/bootstrap.py` and `data/memory_patch.json` to enable live, safe in-memory data updates without risking the core `memory.json`.
- **Synonym Augmentation**: Added `axiom/core/synonyms.py` with regex boundaries to dynamically append canonical math terms to user prompts (e.g. mapping "DL" to "deep learning", "BCE" to "binary cross entropy") before TF-IDF vectorization.
- **Confidence-Based Fallback**: Added a fail-safe to `AxiomOrchestrator` that reroutes mathematically ambiguous queries (cosine score < 0.20) to `chit_chat` before failing out to `unknown`.
- **Memory Auditing Script**: Created `scripts/audit_memory.py` to enforce vocabulary synchronization between Router keywords and Retriever intents.

### Fixed
- Fixed NLP overlapping abbreviations (e.g., "AUC & ROC") by utilizing the synonym augmentation layer.
- Fixed conversational bridging fragments (e.g., "i see", "you were wrong") by adding isolated `gen_acknowledgement` and `gen_feedback` intents, protected by stopword mapping.

## [v2.1.0] - V2 TF-IDF & Robust NLP Upgrades
### Added
- `chit_chat` domain implemented to mathematically handle greetings, identity questions, and general conversation.
- `TF-IDF Vectorizer` implemented purely in NumPy, replacing the basic Binary Bag-of-Words retriever. This penalizes common words (like "learning") and heavily weights rare words (like "SVM").
- Global stopword filtering added to both `router_config.json` and `retriever.py` to prevent common English words from skewing cosine similarities.
- Proprietary `LICENSE` explicitly reserving rights to Divyansh Ailani.

### Fixed
- Fixed overlapping verb collisions (e.g., replaced "how does it work" in ML intents with "operate" to isolate "work" exclusively to the `self` domain).
- Balanced conversational fillers ("whats", "can", "tell") across domains to prevent them from overwhelming specific mathematical keywords.
- Mapped explicit creation verbs ("built", "made", "created") to `chit_chat` identity intents so they aren't stolen by the `history` domain.

## [v1.0.0] - V1 Zero-Training Math Engines (Legacy)
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
