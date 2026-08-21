import pytest

from axiom.orchestrator import AxiomOrchestrator, AxiomInputError
from axiom.core.generator import TemplateGenerator


@pytest.fixture(scope="module")
def orchestrator():
    return AxiomOrchestrator()


def test_type_guard_rejects_non_string(orchestrator):
    for bad in (None, 123, ["hello"], 3.14, b"bytes"):
        resp = orchestrator.chat(bad)
        assert resp.domain == "chit_chat", f"bad input should route to chit_chat, got {resp}"


def test_empty_prompt_graceful(orchestrator):
    for bad in ("", "   ", "\t\n"):
        resp = orchestrator.chat(bad)
        assert "didn't catch" in resp.response_text


def test_chitchat_fallback_updates_confidence(orchestrator):
    # 'you were wrong' should fall back to chit_chat feedback and the reported
    # confidence must be chit_chat's, not the original domain's.
    resp = orchestrator.chat("you were wrong")
    assert resp.domain == "chit_chat"
    assert resp.intent_id == "gen_feedback"
    # confidence must belong to chit_chat, so it should be positive and sane
    assert 0.0 < resp.domain_confidence <= 1.0


def test_greeting_routes_correctly(orchestrator):
    resp = orchestrator.chat("how are you")
    assert resp.domain == "chit_chat"
    assert resp.intent_id == "gen_greeting", f"got {resp.intent_id}"


def test_random_forests_routes_to_new_intent(orchestrator):
    resp = orchestrator.chat("explain random forests")
    assert resp.intent_id == "ml_random_forests", f"got {resp.intent_id}"


def test_transformers_routes_to_modern_context(orchestrator):
    resp = orchestrator.chat("what are transformers")
    assert resp.domain == "modern_context", f"got {resp.domain}"
    assert resp.intent_id == "mod_transformers", f"got {resp.intent_id}"


def test_pipeline_routes_to_self(orchestrator):
    resp = orchestrator.chat("what happens when i ask you a question")
    assert resp.domain == "self"
    assert resp.intent_id == "self_pipeline", f"got {resp.intent_id}"


def test_xgboost_known(orchestrator):
    resp = orchestrator.chat("whats xgboost")
    assert resp.intent_id != "unknown", f"xgboost should be known, got {resp.intent_id}"


def test_responses_are_strictly_known_templates(orchestrator):
    # every generated response must come from an intent's templates, never a
    # hallucinated string
    for q in ["hello", "svm", "who is alan turing", "i see", "thanks"]:
        resp = orchestrator.chat(q)
        assert resp.intent_id != "unknown" or "I don't have knowledge" in resp.response_text
        if resp.intent_id != "unknown":
            intents = orchestrator.memory_dict["domains"][resp.domain]["intents"]
            matched = next(i for i in intents if i["intent_id"] == resp.intent_id)
            assert resp.response_text in matched["response_templates"]


def test_generator_unknown_intent():
    mem = {"domains": {"d": {"intents": []}}}
    gen = TemplateGenerator(mem)
    out = gen.generate("d", "unknown")
    assert "I don't have knowledge" in out


def test_generator_missing_template_branch():
    mem = {"domains": {"d": {"intents": [{"intent_id": "x", "questions": []}]}}}
    gen = TemplateGenerator(mem)
    out = gen.generate("d", "x")
    assert "no response templates" in out