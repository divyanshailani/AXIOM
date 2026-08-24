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

# Contractions tokenize as fragments ("\b\w+\b" splits "doesn't" -> doesn, t),
# so the fragment forms are listed here. Bare "won" is deliberately excluded:
# it collides with the past tense of "win". The apostrophe forms "can't"/
# "won't" reduce to ("can"/"won", "t") pairs whose negation signal sits in the
# dropped single-letter fragment — a documented limitation; "cannot", "can not"
# and the informal "cant" all work.
NEGATORS = {
    "not", "no", "never", "none", "nothing", "nobody", "neither", "nor",
    "without", "cannot", "cant", "wont", "doesn", "don", "didn",
    "isn", "aren", "wasn", "weren",
}

_PREFIX = "not_"


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
    return any(re.search(r"\b" + re.escape(n) + r"\b", text.lower()) for n in NEGATORS)
