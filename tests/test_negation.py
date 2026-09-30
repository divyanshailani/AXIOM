# Copyright (c) 2026 Divyansh Ailani. All Rights Reserved.

from axiom.core.negation import (
    NEGATORS,
    apply_negation_window,
    fold_negated_contractions,
    has_negation,
)


def test_negator_words_are_covered():
    # Contractions arrive as ("X", "t") fragments and are folded by
    # fold_negated_contractions; the folded forms must be negators or
    # "doesn't"-style negation silently stops working.
    for folded in ("doesnt", "dont", "isnt", "wasnt", "cant", "cannot", "wont", "didnt"):
        assert folded in NEGATORS


def test_negated_tokens_keep_plain_forms():
    out = apply_negation_window(["k", "means", "not", "work"])
    assert "work" in out
    assert "not_work" in out


def test_window_limits_negation_scope():
    out = apply_negation_window(["not", "a", "b", "c", "d"], window=3)
    assert "not_a" in out and "not_b" in out and "not_c" in out
    assert "not_d" not in out
    assert "d" in out


def test_no_negator_means_no_prefixed_tokens():
    out = apply_negation_window(["k", "means", "clustering"])
    assert all(not t.startswith("not_") for t in out)


def test_second_negator_restarts_scope():
    out = apply_negation_window(["not", "a", "never", "b"], window=3)
    assert "not_b" in out and "not_a" in out


def test_has_negation_word_boundaries():
    assert has_negation("explain when k-means does not work")
    assert has_negation("it doesn't converge")
    assert not has_negation("explain notable classifiers")


def test_won_is_not_a_negator():
    # 'won' collides with the past tense of win ("who won the world cup");
    # only the folded "won't" form counts.
    assert "won" not in NEGATORS


def test_fold_glues_n_t_fragment_onto_aux_hosts():
    out = fold_negated_contractions(["can", "t", "you", "explain", "svm"])
    assert "cant" in out and "t" not in out and "can" not in out
    out = fold_negated_contractions(["it", "won", "t", "converge"])
    assert "wont" in out


def test_fold_leaves_unrelated_t_fragment_alone():
    # A stray 't' after a non-auxiliary word must not weld onto it.
    out = fold_negated_contractions(["k", "means", "t"])
    assert out == ["k", "means", "t"]
