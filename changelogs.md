# Changelog

All notable changes to the AXIOM project will be documented in this file.

## [v2.4.1] - V2.4.1 Hijack Fix, Contraction Negation, Memory Compaction (Current)
### Fixed
- **Context-retry hijack (measured)**: the V2.4 `standalone_floor` of 0.30 treated any accepted match scoring 0.15-0.30 as "cannot stand alone" and reinterpreted it through the previous turn's topic — "won't that work" (standalone `self_overview` 0.241) was hijacked into `ml_svm` (0.669) after an unrelated SVM turn. The floor is recalibrated to 0.20 from measurements: a genuine follow-up fragment gets accepted at 0.158 against its routed domain, while a hijackable standalone match scored 0.24 — 0.20 separates them. Accepted matches at or above the floor are now never reinterpreted; the follow-up rescues (`"and why is that useful"` 0.837, `"what about its variance"` 0.736) still pass.
- **Apostrophe contractions in negation**: `can't`/`doesn't`/`won't` tokenize as `("can", "t")`/`("doesn", "t")`/`("won", "t")`, so the negation signal sat in the dropped `t` fragment — the documented V2.4 limitation. `negation.fold_negated_contractions()` now glues the fragment back onto its host (restricted to a closed set of contraction hosts, so a stray `t` after an unrelated word can't weld onto it), and `NEGATORS` holds the folded forms. `"explain when k-means doesn't work"` retrieves `ml_clustering` at 0.451 — identical to `"does not work"`. The fold runs in both the router and the retriever tokenizers, so bare `won` no longer leaks into the router vocabulary either.
### Added
- **Memory compaction tool**: `scripts/compact_memory.py --apply` squashes the `memory_patch.json` transaction log into `memory.json` (32 patches applied, log verified idempotent against the merged state, refuses while either memory file has uncommitted changes). The shipped log was compacted: `memory.json` at `memory_version` 2.4 now contains the full post-V2.4 state (26 intents across 5 domains), and boot replays an empty log. New intents should still ship as patches; compact once they're regression-tested.
### Fixed (housekeeping)
- Removed duplicate `"machine learning"` / `"artificial intelligence"` keys in `synonyms.ML_SYNONYMS` (second pair shadowed the first).
- Deleted the stale root `test_edge_cases.py`: a V2.1 print-only script, collected zero pytest tests, fully superseded by `tests/`.
- README now says how to actually run the project: the local `.venv/` (the system python has no numpy/pytest).

## [v2.4.0] - V2.4 Calibration & Multi-Turn
All threshold decisions in this release are measurement-driven: every golden
question in memory and a battery of adversarial queries were scored through
the live pipeline before picking numbers.

### Added
- **Strict-evidence retrieval**: the retriever's fuzzy mapper now only trusts *containment* (a vocabulary word appearing inside the query token: "svmm" contains "svm", "transformers" contains "transformer"). Loose char-trigram coincidence was measured producing confident nonsense — zero-overlap queries like "what is the weather" or "gradient descent" scored 0.35-0.60 against unrelated intents, *higher* than legitimate queries. Coincidental n-grams can no longer justify an answer.
- **Ambiguity margin**: `ambiguity_margin` (retriever_config) rejects an intent that fails to beat its runner-up by a relative gap — near-ties now fall back honestly instead of answering whichever came out on top.
- **Context retry (multi-turn)**: when a query cannot stand on its own (score below `context_retry.standalone_floor`), the orchestrator retries retrieval over previous-query + current-query so pronoun follow-ups ("what about its variance?" after SVM talk) resolve against the established topic. Three gates prevent hijacking legitimate standalone answers: chit_chat turns are never reinterpreted, adoption requires clearing `min_score`, and the merged match must hold at least twice the primary evidence. `ConversationBuffer` is now load-bearing instead of write-only.
- **Miss log**: fallbacks append `{timestamp, query, reason, routed domain, router top-3, best intent, score, runner-up}` to `data/miss_log.jsonl` (path via `miss_log_path` config; set to null to disable). Reason codes distinguish `empty_query` / `below_threshold` / `ambiguous` / `no_model`, making future tuning data-driven.
- **Negation windows**: tokens after a negator ("not", "never", "doesn"…) additionally emit prefixed variants ("not_work") in both router and retriever vocabularies, so "explain when k-means does NOT work" stays inside clustering instead of order-blindly routing to self-overview. Plain forms are kept alongside, so non-negated matching is unchanged. Shared helper: `axiom/core/negation.py`. Known limitation: the apostrophe forms "can't"/"won't" tokenize as ("can"/"won", "t") whose negation signal sits in the dropped single-letter fragment — use "cannot"/"not"/"cant".
- **Gradient descent intent**: added `ml_gradient_descent` via memory patch. Calibration showed no threshold separates it from legitimate queries (it shares the real word "gradient" with gradient-boosting docs); coverage is the classical fix for its most common phrasing.
- **New tests**: negation unit tests, margin/strict-evidence retrieval tests, miss-log test, retriever-caching regression, context-retry rescue-and-hijack-guard cases, punctuation input, patch idempotency (77 total).

### Fixed
- Fixed confident wrong answers from trigram noise: "what is the weather", "explain quantum computing", "recommend me a movie", "what about its variance" all answered unrelated templates at 0.35-0.60; they now fall back honestly (and follow-ups among them resolve through context retry).
- Fixed punctuation-only input ("!!!") producing a dishonest "I don't have knowledge about topics in 'classical_ml'" apology; content-free prompts now return "I didn't catch that."
- Fixed per-message rebuild cost: `IntentRetriever` instances (TF-IDF models + config parsing) are built once per domain at boot, not on every chat call.
- Fixed `memory_patch.json` replays duplicating data: `add_questions` and `add_router_keywords` are idempotent (duplicates within one patch are also skipped).
- Fixed audit drift: key_terms vocabulary (hyperplane, centroid, margin, axiom, tfidf, …) is now covered by router keywords via memory patches; `scripts/audit_memory.py` reports clean. 'k' is exempted in the audit (below router `min_word_length` by design).
- Fixed dead config keys (`enable_explanations`, `response_format`, `glove_path`, `vectorization`) — removed. `memory_path` is now actually wired into `MemoryBootstrap`; `miss_log_path` and `context_retry` are new wired keys. A config regression test keeps them honest.

### Known limitations (measured, documented)
- Single-word lexical collisions remain possible classically: "who won the world cup" matches identity questions on the real word "who"; "tell me about football" matches gen_joke on "tell". No BoW system can separate these without semantics or knowledge coverage; miss logging surfaces them for future intents.
- Standalone orphan fragments with no prior turn ("and why is that useful") may still weak-match a generic template; with prior context they resolve correctly.

## [v2.3.0] - V2.3 Hardening & NLP Coverage
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
