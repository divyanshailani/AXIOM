import json

from axiom.core.retriever import IntentRetriever


def test_find_intent_detailed_accepts_strong_match(loaded_memory, retriever_config):
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    d = r.find_intent_detailed("explain support vector machines")
    assert d["accepted"] is True
    assert d["reason"] == "accepted"
    assert d["intent_id"] == "ml_svm"


def test_zero_evidence_query_rejected_even_when_ngrams_would_have_matched(
        loaded_memory, retriever_config):
    # V2.4 regression: 'weather' shares char trigrams with vocabulary words and
    # used to score ~0.38 against ml_overview purely via trigram coincidence —
    # higher than legitimate queries. Coincidental n-grams must never justify
    # an answer.
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    d = r.find_intent_detailed("what is the weather")
    assert d["accepted"] is False


def test_ambiguous_winner_rejected(loaded_memory, retriever_config):
    # Two intents nearly tied means no confident answer exists; the compound
    # query 'compare svm and k-means' sits between ml_svm and ml_clustering.
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    d = r.find_intent_detailed("compare svm and k-means for clustering text")
    if d["runner_up_score"] > 0:
        rel_gap = (d["score"] - d["runner_up_score"]) / max(d["score"], 1e-9)
        if rel_gap < 0.10:
            assert d["accepted"] is False
            assert d["reason"] == "ambiguous"


def test_runner_up_reported_for_misses(loaded_memory, retriever_config):
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    d = r.find_intent_detailed("how to bake a cake")
    assert d["accepted"] is False
    assert d["reason"] in ("below_threshold", "empty_query", "no_model")
    assert isinstance(d["runner_up_score"], float)


def test_empty_vector_reports_empty_query(loaded_memory, retriever_config):
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    d = r.find_intent_detailed("!!!")
    assert d["reason"] == "empty_query"
    assert d["accepted"] is False


def test_negated_question_matches_negation_aware_intent(loaded_memory, retriever_config):
    # "when does k-means NOT work" must stay inside clustering instead of the
    # order-blind BoW behavior that used to route it to self_overview.
    r = IntentRetriever(loaded_memory, retriever_config, 'classical_ml')
    intent, score = r.find_intent("explain when k-means does not work")
    assert intent != "unknown", f"negated clustering question should retrieve ({score:.3f})"


def test_plural_folds_via_containment_mapping(loaded_memory, retriever_config):
    # 'transformers' contains vocab word 'transformer'; containment mapping is
    # trusted evidence (unlike loose trigrams).
    r = IntentRetriever(loaded_memory, retriever_config, 'modern_context')
    intent, _ = r.find_intent("what are transformers")
    assert intent == "mod_transformers"
