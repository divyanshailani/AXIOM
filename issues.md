# AXIOM Edge Cases & Known Issues

This document tracks edge cases discovered through CLI and automated testing.

## Status Update (V2.3, 2026-08-21)

All five V2.1 issues below were resolved in V2.2 (via `memory_patch.json`, synonym augmentation, and the confidence-based fallback), and are now **guarded by regression tests** in `tests/`. V2.3 additionally fixed the following V2.2-era gaps:

### V2.3 Resolved Issues
1. **All-stopword query OOV**: `"how are you"` matched `unknown` (0.00) because `how`/`are`/`you` are all stopwords and the query collapsed to nothing. Fixed by falling back to raw words in the retriever when stopword filtering empties the token stream.
2. **Transformers misrouting**: `"what are transformers"` routed to `chit_chat`/`unknown` because the `modern_context` prior (0.10) was too low and no transformer router keywords existed on the patched memory. Fixed by recalibrating priors and adding transformer/attention keywords.
3. **Key-terms dead field**: `key_terms` (e.g. "xgboost", "kernel trick", "auc") was read by nothing, so those terms were unmatchable. Fixed: retriever now folds key_terms into the TF-IDF vocabulary.
4. **Random-forest conflation**: `"explain random forests"` answered with decision-tree text. Fixed with a dedicated `ml_random_forests` intent.
5. **Pipeline vs architecture conflation**: `"how do you work"` answered with the Naive-Bayes router description. Fixed with a dedicated `self_pipeline` intent.
6. **Near-miss tokens**: `"hiii"` / `"svmm"` fell to `unknown` despite being obvious typos. Fixed via char n-gram tolerance (config-gated, default on).
7. **Conversational thanks**: `"thanks"` / `"thank you"` fell to `unknown`. Fixed with a dedicated `gen_thanks` intent.
8. **Single-letter expansion collision**: adding `"k"` to the "okay" casual synonyms caused `"k means"` / `"knn"` queries to expand to "okay" and be hijacked by chit_chat. Fixed by removing `"k"` from okay-variants (regression-tested).

### Known Remaining Gaps (advisory)
- The router treats a zero-token query as the prior distribution; the orchestrator's empty-prompt guard means this only shows for punctuation-only input like `"!!!"`, which returns the generic apology. Acceptable, but could be tightened.
- Knowledge coverage is limited to what's curated in `memory.json` + patches. Terms like "hyperplane", "margin", "centroid" exist in intent key_terms but are not router keywords, so a user typing them bare may route to the highest-prior domain. See `python scripts/audit_memory.py` for the full drift report.
- The char n-gram feature is a heuristic tuned for short ML vocab; it may add slight noise on very short queries. It is config-gated (`use_char_ngrams`).

---

## V2.1 Issues (all Fixed in V2.2, regression-guarded since V2.3)

## 1. Abbreviation & Synonym OOV (Out of Vocabulary)
- **Input**: `"& what's DL ?"`
- **Result**: Routed to `classical_ml`, matched `unknown` (Score: 0.00).
- **Issue**: "DL" is not in the vocabulary. The engine knows "deep learning" under `modern_context`, but fails on the abbreviation "DL". Because it's OOV, the router falls back to the highest prior (`classical_ml` at 0.35).
- **Fix Required**: Add "DL" to `modern_context` router keywords and intent questions.

## 2. Accidental Intent Triggering via Common Verbs
- **Input**: `"i see"`
- **Result**: Routed to `chit_chat`, matched `gen_farewell` (Score: 0.41).
- **Issue**: The word "see" mathematically triggers the "see you later" farewell intent because "see" has a high TF-IDF weight in that small document.
- **Fix Required**: Add an explicit `gen_acknowledgement` intent (e.g., "i see", "got it", "okay") to `chit_chat` to catch conversational acknowledgments, or add "see" to stopwords.

## 3. Missing Router Keywords for Valid Intents
- **Input**: `"explain your architecture"`
- **Result**: Routed to `classical_ml`, matched `unknown` (Score: 0.00).
- **Issue**: "explain" is heavily weighted towards `classical_ml` ("explain svm", "explain knn"). "architecture" exists in the `self` domain's *retriever* intents, but it was NEVER added to the `self` domain's *router keywords*. Thus, the router ignores "architecture" and blindly routes based on "explain".
- **Fix Required**: Add "architecture" and "explain" to `self` router keywords in `memory.json`.

## 4. Advanced ML Terminology Missing
- **Input**: `"binary cross entropy ?"`
- **Result**: Routed to `classical_ml`, matched `ml_decision_trees` (Score: 0.23).
- **Issue**: The engine sees "entropy" and mathematically links it to decision trees ("what is entropy in a decision tree"). It lacks knowledge of "cross entropy" for logistic regression.
- **Fix Required**: Add "cross entropy" and "binary cross entropy" to `ml_logistic_regression`.

- **Input**: `"AUC & ROC ?"`
- **Result**: Routed to `classical_ml`, matched `unknown` (Score: 0.00).
- **Issue**: ROC and AUC are completely missing from the vocabulary.
- **Fix Required**: Add "AUC" and "ROC" to `ml_logistic_regression`.

## 5. Error Handling & Correction
- **Input**: `"you were wrong"`
- **Result**: Routed to `classical_ml`, matched `unknown` (Score: 0.00).
- **Issue**: The engine has no concept of user corrections. "wrong" is OOV.
- **Fix Required**: Add a `gen_feedback` or `gen_correction` intent to `chit_chat` to gracefully handle "you are wrong", "incorrect", "my bad".
