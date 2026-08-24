import json

import pytest

from axiom.orchestrator import AxiomOrchestrator


@pytest.fixture()
def orc():
    return AxiomOrchestrator()


def test_retrievers_cached_not_rebuilt_per_message(orc):
    # V2.4 regression: IntentRetriever used to be constructed inside chat(),
    # re-parsing configs and recomputing TF-IDF on every message.
    first = orc._retrievers['classical_ml']
    orc.chat("explain svm")
    assert orc._retrievers['classical_ml'] is first
    assert set(orc._retrievers) == set(orc.memory_dict['domains'])


def test_punctuation_only_input_gets_honest_response(orc):
    # '!!!' has no readable content; it must not produce a domain apology
    # claiming we lack knowledge about e.g. 'classical_ml'.
    for junk in ("!!!", "???", "...", "@#$%"):
        resp = orc.chat(junk)
        assert "didn't catch" in resp.response_text
        assert resp.intent_id == "gen_feedback"


def test_context_retry_rescues_followup_fragment(orc):
    orc.chat("explain k means clustering")
    resp = orc.chat("and why is that useful")
    assert resp.intent_id == "ml_clustering", f"follow-up lost: {resp}"


def test_context_retry_rescues_pronoun_followup(orc):
    orc.chat("explain svm")
    resp = orc.chat("what about its variance")
    assert resp.domain == "classical_ml"
    assert resp.intent_id != "unknown"


def test_complete_query_survives_unrelated_prior_topic(orc):
    # The retry must not hijack queries that stand on their own, even when a
    # strong unrelated topic precedes them.
    orc.chat("explain random forests")
    resp = orc.chat("what are transformers")
    assert resp.domain == "modern_context", f"hijacked by prior topic: {resp}"


def test_chitchat_never_reinterpreted_through_prior_topic(orc):
    orc.chat("explain svm")
    resp = orc.chat("how are you today")
    assert resp.intent_id == "gen_greeting", f"social turn hijacked: {resp}"


def test_miss_log_written_on_fallback(orc, tmp_path):
    log_path = tmp_path / "misses.jsonl"
    orc.miss_log_path = log_path
    orc.chat("explain quantum computing")
    assert log_path.exists()
    entry = json.loads(log_path.read_text().splitlines()[0])
    assert entry["query"] == "explain quantum computing"
    assert entry["reason"] in ("empty_query", "below_threshold", "ambiguous", "no_model")
    assert "best_intent" in entry and "score" in entry
    assert len(entry["router_top3"]) == 3


def test_miss_log_disabled_when_path_null(orc):
    orc.miss_log_path = None
    resp = orc.chat("explain quantum computing")
    assert resp.intent_id == "unknown"
