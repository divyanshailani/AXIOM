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
    "neural network": ["nn"]
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
    
    if extras:
        return text + " " + " ".join(extras)
    return text
