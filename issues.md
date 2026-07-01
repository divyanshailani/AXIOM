# Known Issues (V1 Zero-Training Pipeline)

## 1. General Conversation & Chit-Chat Missing
- **Issue**: The bot cannot handle general greetings ("hello", "hey", "how are you") or small talk. It tries to force them into technical domains or returns `unknown`.
- **Cause**: The `memory.json` does not contain a `general` or `chit_chat` domain. Unknown words fall back to the domain with the highest base probability (currently `classical_ml`).
- **Solution**: Add a `chit_chat` domain to memory with common greetings, identity questions, and responses.

## 2. Brittle Vocabulary (No Semantic Understanding)
- **Issue**: Synonyms and related phrasing fail. For example, "classical ML" routes to `modern_context` because those exact words only appeared in a question about "classical ml vs deep learning". "maths" or "xgboost" fail completely because they aren't in the vocabulary.
- **Cause**: Naive Bayes and Binary Bag-of-Words rely on **exact lexical matches**. We do not yet use dense embeddings (like Word2Vec/GloVe), so the engine doesn't mathematically know that "math" is related to "regression".
- **Solution**: 
  - **Short term**: Expand the `questions` and `router_keywords` arrays in `memory.json` to include many synonyms and variations.
  - **Long term**: Upgrade the Retriever to use GloVe embeddings or TF-IDF with cosine similarity instead of simple Jaccard-like Bag-of-Words.

## 3. Overlapping Keyword Collisions
- **Issue**: The query "machine learning" matched the `ml_clustering` intent because of the word "learning" in "unsupervised learning".
- **Cause**: Binary Bag-of-Words gives equal weight to all words. The word "learning" is very common, but it shouldn't trigger a highly specific clustering response just because they share one word.
- **Solution**: Implement **TF-IDF (Term Frequency-Inverse Document Frequency)** so common words like "learning" get mathematically down-weighted, and rare words like "clustering" or "svm" get massive up-weights in the vector space.
