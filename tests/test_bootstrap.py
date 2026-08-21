import json

import pytest

from axiom.bootstrap import MemoryBootstrap


@pytest.fixture(scope="module")
def bootstrap(tmp_path_factory):
    # Build an in-memory fake repo to test the bootstrap without touching the
    # real data directory.
    base = tmp_path_factory.mktemp("axiom_bootstrap")
    (base / "data").mkdir()
    base_memory = {
        "memory_version": "test",
        "domains": {
            "d": {
                "router_keywords": ["alpha"],
                "intents": [
                    {"intent_id": "i1", "questions": ["q1"], "response_templates": ["r1"], "key_terms": []}
                ],
            }
        },
    }
    with open(base / "data" / "memory.json", "w") as f:
        json.dump(base_memory, f)
    return MemoryBootstrap(base)


def _write_patch(bootstrap, patches):
    with open(bootstrap.patch_path, "w") as f:
        json.dump({"patches": patches}, f)


def test_no_patch_file_returns_base(bootstrap):
    mem = bootstrap.load_memory()
    assert "alpha" in mem["domains"]["d"]["router_keywords"]


def test_add_questions_patch(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "add_questions", "intent_id": "i1", "questions": ["q2", "q3"]}
    ])
    mem = bootstrap.load_memory()
    assert "q2" in mem["domains"]["d"]["intents"][0]["questions"]


def test_add_intent_patch(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "add_intent",
         "intent": {"intent_id": "i2", "questions": ["nq"], "response_templates": ["nr"], "key_terms": []}}
    ])
    mem = bootstrap.load_memory()
    ids = [i["intent_id"] for i in mem["domains"]["d"]["intents"]]
    assert "i2" in ids


def test_add_router_keywords_patch(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "add_router_keywords", "keywords": ["beta", "gamma"]}
    ])
    mem = bootstrap.load_memory()
    assert "beta" in mem["domains"]["d"]["router_keywords"]


def test_unknown_domain_raises(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "nope", "action": "add_router_keywords", "keywords": ["x"]}
    ])
    with pytest.raises(ValueError, match="unknown domain"):
        bootstrap.load_memory()


def test_unknown_action_raises(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "delete_everything"}
    ])
    with pytest.raises(ValueError, match="unknown action"):
        bootstrap.load_memory()


def test_malformed_intent_raises(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "add_intent", "intent": {"questions": ["no id"]}}
    ])
    with pytest.raises(ValueError, match="intent_id"):
        bootstrap.load_memory()


def test_unknown_intent_for_questions_raises(bootstrap):
    _write_patch(bootstrap, [
        {"domain": "d", "action": "add_questions", "intent_id": "missing", "questions": ["x"]}
    ])
    with pytest.raises(ValueError, match="unknown intent"):
        bootstrap.load_memory()


def test_real_patch_file_applies():
    # Point at the real repo data dir to confirm the shipped V2.2+V2.3 patches
    # load and produce the expected intents.
    from pathlib import Path
    repo_root = Path(__file__).parent.parent
    real = MemoryBootstrap(repo_root)
    mem = real.load_memory()
    chit = [i["intent_id"] for i in mem["domains"]["chit_chat"]["intents"]]
    assert "gen_acknowledgement" in chit
    assert "gen_feedback" in chit
    assert "gen_thanks" in chit
    ml = [i["intent_id"] for i in mem["domains"]["classical_ml"]["intents"]]
    assert "ml_random_forests" in ml
    self_ids = [i["intent_id"] for i in mem["domains"]["self"]["intents"]]
    assert "self_pipeline" in self_ids