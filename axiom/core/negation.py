# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.
# This file is part of AXIOM and is proprietary and confidential.

"""Shared negation-window handling for the router and retriever.

Bag-of-Words is order-blind, so "when does k-means work" and "when does
k-means NOT work" produce identical vectors. We stay fully classical: tokens
inside a small window after a negator are additionally emitted in a prefixed
form ("not_work"), so negated phrases become distinguishable vocabulary while
the original tokens are kept (queries and documents that do not use negation
still match each other exactly as before).
"""

import re

# The "\b\w+\b" tokenizer splits apostrophe contractions into fragments
# ("can't" -> can, t; "doesn't" -> doesn, t), so fold_negated_contractions()
# first glues a stray "t" fragment back onto its host word ("cant", "doesnt")
# and the negators below are the folded forms. Bare "won" is deliberately
# excluded: it collides with the past tense of "win" ("who won the world
# cup"); only the folded "wont" counts as a negator.
NEGATORS = {
    "not", "no", "never", "none", "nothing", "nobody", "neither", "nor",
    "without", "cannot", "cant", "wont", "shant", "dont", "doesnt", "didnt",
    "isnt", "arent", "wasnt", "werent", "couldnt", "shouldnt", "wouldnt",
    "mustnt", "havent", "hadnt", "neednt", "darent",
}

_PREFIX = "not_"

# Closed set of auxiliary/modal stems that can precede the n't fragment in
# English. Restricting the fold to these hosts keeps a stray single-letter
# "t" from welding onto unrelated words ("k means" would otherwise produce
# the garbage token "meanst").
_AUX_HOSTS = {
    # Contraction hosts exactly as the tokenizer emits them: "doesn't"
    # arrives as ("doesn", "t"), "can't" as ("can", "t"), "won't" as
    # ("won", "t"). Only these absorb a following "t" fragment.
    "can", "won", "shan", "couldn", "shouldn", "wouldn", "mightn", "mustn",
    "don", "doesn", "didn", "isn", "aren", "wasn", "weren", "haven", "hadn",
    "needn", "daren",
}


def fold_negated_contractions(tokens: list) -> list:
    """Glues an n't fragment onto its auxiliary host ("can" + "t" -> "cant").

    Apostrophes are word boundaries for "\b\w+\b", so every English
    X-n't contraction arrives as ("X", "t") and its negation signal sat in
    the dropped single-letter fragment. Folding restores "cant"/"wont"/
    "doesnt" as single tokens the NEGATORS set can actually match, in both
    the router and the retriever. Only _AUX_HOSTS words absorb the fragment,
    so unrelated tokens followed by a stray "t" stay intact.
    """
    out = []
    for tok in tokens:
        if tok == "t" and out and out[-1] in _AUX_HOSTS:
            out[-1] += "t"
        else:
            out.append(tok)
    return out


def apply_negation_window(tokens: list, window: int = 3) -> list:
    """Returns tokens plus prefixed variants for negation-scoped tokens.

    Both the plain token and its 'not_' variant are kept for tokens inside the
    window, so non-negated matching is preserved and negation becomes extra
    discriminative signal instead of a replacement. A negator inside another's
    window restarts the scope rather than nesting prefixes.
    """
    out = []
    remaining = 0
    for tok in tokens:
        if tok in NEGATORS:
            remaining = window
            continue
        out.append(tok)
        if remaining > 0:
            out.append(_PREFIX + tok)
            remaining -= 1
    return out


def has_negation(text: str) -> bool:
    """True if any standalone negator appears in the raw text."""
    words = re.findall(r"\b\w+\b", text.lower())
    return any(w in NEGATORS for w in fold_negated_contractions(words))
