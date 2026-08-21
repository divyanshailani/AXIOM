# Changelog

All notable changes to the AXIOM project will be documented in this file.

## [v2.3.0] - V2.3 Hardening & NLP Coverage (Current)
### Added
- **Random forests intent**: Added `ml_random_forests` to `classical_ml` via memory patch so "explain random forests" gets a dedicated answer instead of falling back to decision-tree text.
- **Pipeline intent**: Added `self_pipeline` to `self` via memory patch so "how do you work" / "what happens when i ask you a question" get a step-by-step answer.
- **Thanks intent**: Added `gen_thanks` to `chit_chat` for "thanks", "thank you", "thx".
- **Greeting variants**: Added "how are you", "hi there", "whats up" and friends to `gen_greeting` and chit_chat router keywords.
- **Key-terms into the retriever**: `key_terms` on intents now feed the TF-IDF vocabulary, so terms like "xgboost", "kernel trick", "auc" that only appeared in metadata are finally matchable.
- **Char n-gram tolerance**: config-gated char n-gram features let near-miss tokens ("hiii" -> hi, "svmm" -> svm) contribute fuzzy signal without expanding the vocabulary; short vocab words only match as a token prefix so stray letters inside unrelated words never vote.
- **Input hardening**: non-string prompts and empty/whitespace input return a graceful response instead of crashing or fake-routing by priors; Ctrl-D in the CLI now exits cleanly.
- **Config-driven fallbacks**: the orchestrator reads `similarity_threshold` and the new `chitchat_admission` from `retriever_config.json` instead of hardcoding 0.20/0.25.
- **Patch validation**: `MemoryBootstrap` now raises `ValueError` on unknown domains, unknown actions, malformed intents, and unknown intent_ids instead of silently no-op'ing.
- **Test infrastructure**: restored the 3 broken pytest tests (constructor signature) and added 47 unit/integration tests (router, retriever, synonyms, orchestrator, bootstrap, generator, conversation buffer, config invariants, CLI).
- **Assert-based harness**: `run_tests.py` now checks routing goldens for all 51 prompts and exits non-zero on failure, instead of just recording output.
- **Patch-aware audit**: `scripts/audit_memory.py` now loads base + patch memory and reports intent vocabulary the router genuinely cannot see.

### Fixed
- Fixed `how are you` matching `unknown` (all-stopword phrase now falls back to raw tokens in the retriever).
- Fixed `what are transformers` misrouting to `chit_chat` (router prior recalibration + transformer keywords).
- Fixed `whats xgboost` matching `unknown` (now routes via key_terms).
- Fixed `how does k means work` and `knn`-family queries being hijacked by the chit_chat fallback (single-letter `k` no longer expands to "okay").
- Fixed the stale-confidence bug: when the chit_chat fallback adopts a new domain, the reported confidence now belongs to chit_chat, not the original domain.
- Fixed `ConversationBuffer` with `max_length=0` not trimming.
- Fixed dead code: removed unused `get_context`, unused `sys` import, redundant double stopword filtering in the router.

### Changed
- Router prior for `modern_context` raised 0.10 -> 0.15, `history` lowered 0.15 -> 0.10, to reflect current intent coverage.
- Reduced `retriever_config` stopwords (removed "whats") so contractions can match.
- README corrected: AXIOM uses strict templated generation, not a Markov chain (docs-honesty fix).

## [v2.2.0] - V2 Meta-Fix & NLP Robustness
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
