# NLP Edge Cases: Proposed Solutions

This document catalogs the structural and data-driven solutions for the NLP edge cases identified in `issues.md`, based on the provided engineering designs.

## Issue 1: Abbreviation & Synonym OOV ("DL")
**Problem**: The engine fails on abbreviations like "DL" because it relies entirely on exact lexical matching. It has zero probability for "DL" since it's an Out-Of-Vocabulary (OOV) token.

**Solution**:
1. **Structural Fix (Code)**: Implement an `Abbreviation Expander` in a new file `axiom/core/preprocessor.py`. This layer runs *before* the router and uses a dictionary to map abbreviations to their full forms:
   - `"dl"` -> `"deep learning"`
   - `"nn"` -> `"neural network"`
   - `"svm"` -> `"support vector machine"`
   - `"auc"` -> `"area under curve"`
   - `"roc"` -> `"receiver operating characteristic"`
   - etc.
   By running this preprocessor in `orchestrator.py` before routing, the entire mathematical pipeline benefits without needing to duplicate abbreviations across the JSON memory.
2. **Quick Fix (Data)**: Add specific questions like `"what is DL"` and `"explain DL"` to the `mod_transformers` intent in `memory.json`, and add `"DL"` to the `modern_context` router keywords. *(Note: The structural preprocessor makes this largely redundant, but it serves as a safety net).*

## Issue 2: Accidental Intent Triggering ("i see")
**Problem**: The phrase "i see" mathematically matches the `gen_farewell` intent because the word "see" has a high TF-IDF weight from the phrase "see you later". Since it's the only matching word, it dominates the score.

**Solution**:
1. **Structural Fix (Code)**: Add `"see"`, `"i"`, and `"it"` to the router stopwords in `data/router_config.json`. "See" carries no discriminative power for determining domains (like ML vs. History), so removing it prevents the router from being skewed. 
2. **Quick Fix (Data)**: Add a new `gen_acknowledgement` intent to the `chit_chat` domain in `memory.json`. 
   - **Questions**: `"i see"`, `"got it"`, `"okay"`, `"alright"`, `"understood"`, `"makes sense"`
   - **Response Templates**: `"Glad that makes sense."`, `"Understood. Let me know if you have another question."`, `"Acknowledged. What would you like to explore next?"`
   - **Key Terms**: `"see"`, `"got"`, `"okay"`, `"understood"`
   
   Because the retriever uses a separate stopword list (or processes the full phrase differently depending on the configuration), the phrase "i see" will still successfully match the new `gen_acknowledgement` intent via cosine similarity, while the router safely ignores it.

## Issue 3: Missing Router Keywords ("explain your architecture")
**Problem**: The Router acts as a gatekeeper based on its training vocabulary. The word "architecture" was present in the `self` domain's intent questions, but missing from its `router_keywords`. The router only saw "explain" and pushed the query to `classical_ml`.

**Solution**:
1. **Quick Fix (Data)**: Add the missing vocabulary to the `self` domain's `router_keywords`: `"architecture"`, `"explain"`, `"how are you built"`, `"your design"`, `"your code"`, `"your logic"`, `"your pipeline"`.
2. **Structural Fix (Process)**: Implement a `scripts/audit_memory.py` utility script to automatically catch these discrepancies in the future. The script loads `memory.json`, extracts all unique words from the intent `questions`, and compares them against the `router_keywords`. It then logs any intent words that the router is blind to, preventing manual sync errors.

## Issue 4: Advanced ML Terminology Missing ("binary cross entropy", "AUC & ROC")
**Problem**: The math engine's knowledge is entirely dependent on its curated JSON dictionary. It has no generalized understanding of ML, so terms like "AUC", "ROC", and "binary cross entropy" were treated as completely unknown, causing the router to misclassify them or the retriever to fail.

**Solution**:
1. **Structural Fix (Code)**: Implement a `Synonym/Augmentation Layer` (`axiom/core/synonyms.py`). Unlike the simple abbreviation replacer, this script maps canonical ML terms to a list of variants (e.g., `"binary cross entropy": ["cross entropy", "bce", "log loss"]`). When a user types a variant, the script *appends* the canonical form to the query string before it hits the vectorizer. For example, `"AUC & ROC ?"` becomes `"AUC & ROC ? area under curve receiver operating characteristic"`. This drastically increases the TF-IDF hit rate without needing to manually add 50 variations of every question to `memory.json`.
2. **Quick Fix (Data)**: Add the specific missing questions (`"what is binary cross entropy"`, `"explain AUC and ROC"`, etc.) to the `ml_logistic_regression` intent in `memory.json`. Also, add the canonical terms to the `classical_ml` router keywords so the Naive Bayes router has mathematical awareness of them.

## Issue 5: Error Handling & Correction ("you were wrong")
**Problem**: The math engine has no concept of conversational repair. If a user corrects it ("you are wrong", "incorrect"), the router treats those words as unknown ML terms, forcing them into a fallback ML domain, which fails.

**Solution**:
1. **Quick Fix (Data)**: Add a new `gen_feedback` intent to the `chit_chat` domain in `memory.json` to catch phrases like `"you are wrong"`, `"that is incorrect"`, `"my bad"`. Add the words `"wrong"`, `"incorrect"`, `"mistake"`, `"bad"` to the `chit_chat` router keywords so Naive Bayes correctly routes corrections.
2. **Structural Fix (Code)**: Implement a `Confidence-Based Fallback` in the `AxiomOrchestrator` (`axiom/orchestrator.py`). If the initial routing domain yields a very low retriever confidence (`cosine_score < 0.20`), the orchestrator will automatically attempt to retrieve against the `chit_chat` domain as a safety net. If `chit_chat` finds a match with a higher threshold (`>= 0.25`), it dynamically overrides the initial domain choice. This prevents conversational fragments from being forced into technical domains just because they lacked strong router keywords.

## The Meta-Fix: Production Memory Patching
**Problem**: The "Quick Fixes" for all five issues involved directly editing `memory.json`. Editing the core knowledge dictionary directly is error-prone and doesn't scale for live production systems. It risks corrupting the base memory matrix.

**Solution**:
1. **Data Separation**: Introduce `data/memory_patch.json`. This file acts as a transaction log of live corrections. Instead of editing `memory.json`, we append JSON patch objects containing the date, domain, action (e.g., `add_questions`, `add_intent`), and the data payload.
2. **Bootstrap Script (`axiom/bootstrap.py`)**: Implement a memory loader that reads `memory.json` as a base, then iterates through `memory_patch.json` and dynamically applies the patches in-memory at startup. 
   - **Why this matters**: We can now rapidly deploy fixes for edge cases (like OOV words or missing intents) safely in production, leaving an explicit audit trail of what the engine has "learned" over time without touching the base source of truth.
