# AXIOM V2.1 NLP Edge Cases & Known Issues

Based on the latest CLI testing, the Naive Bayes Router and TF-IDF Retriever have made significant improvements in structural intent separation, but they still struggle with specific vocabulary collisions and Out-Of-Vocabulary (OOV) fallbacks. 

This document outlines the current failures to be addressed by the next agent.

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
