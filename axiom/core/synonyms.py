# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

import re

ML_SYNONYMS = {
    "binary cross entropy": ["cross entropy", "bce", "log loss"],
    "support vector machine": ["svm", "support vector"],
    "logistic regression": ["logistic", "logit", "sigmoid classifier"],
    "k nearest neighbors": ["knn", "nearest neighbor"],
    "area under curve": ["auc", "auroc"],
    "receiver operating characteristic": ["roc", "roc curve"],
    "deep learning": ["dl", "deep neural network"],
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "neural network": ["nn"],
}

# Casual / contraction forms that the byte-level stemmer cannot fold because
# they are dictionary words in their own right (e.g. 'u' is a real word).
# NOTE: 'k' is deliberately excluded from okay-variants — it collides with
# k-means / k-nearest-neighbors in ML queries.
CASUAL_SYNONYMS = {
    "you": ["u", "ya"],
    "are": ["r", "ru"],
    "what is": ["whats"],
    "give me": ["gimme"],
    "thanks": ["thx", "ty", "thanx"],
    "please": ["plz", "pls"],
    "i do not know": ["idk"],
    "okay": ["ok", "kk", "alright"]
}

def augment_query(text: str) -> str:
    """Appends canonical forms to the query for better matching."""
    text_lower = text.lower()
    extras = []
    
    # Use word boundaries to prevent substring matches (e.g. 'dl' in 'handle')
    for canonical, variants in ML_SYNONYMS.items():
        for v in variants:
            if re.search(r'\b' + re.escape(v) + r'\b', text_lower):
                extras.append(canonical)
                break  # only append once per canonical form
    
    for canonical, variants in CASUAL_SYNONYMS.items():
        for v in variants:
            if re.search(r'\b' + re.escape(v) + r'\b', text_lower):
                extras.append(canonical)
                break
    
    if extras:
        return text + " " + " ".join(extras)
    return text
