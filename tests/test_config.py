import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def test_router_priors_sum_to_one():
    with open(BASE_DIR / "data" / "router_config.json") as f:
        cfg = json.load(f)
    priors = cfg["domain_priors"]
    assert abs(sum(priors.values()) - 1.0) < 1e-9, f"priors must sum to 1, got {priors}"


def test_router_priors_cover_all_domains(loaded_memory):
    with open(BASE_DIR / "data" / "router_config.json") as f:
        cfg = json.load(f)
    domains = set(loaded_memory["domains"].keys())
    assert set(cfg["domain_priors"].keys()) == domains


def test_fallback_thresholds_live_in_config_not_code():
    # single source of truth: the orchestrator reads these from config; the
    # code must not hardcode different numbers.
    with open(BASE_DIR / "data" / "retriever_config.json") as f:
        cfg = json.load(f)
    assert cfg["similarity_threshold"] == 0.15
    assert cfg["chitchat_admission"] == 0.25
    assert cfg["fallback_intent"] == "unknown"
    assert 0 <= cfg["ambiguity_margin"] < 1


def test_dead_config_keys_stay_gone():
    # V2.4 honesty regression: these keys were declared but read nowhere.
    with open(BASE_DIR / "data" / "orchestrator_config.json") as f:
        orch = json.load(f)
    assert "enable_explanations" not in orch
    assert "response_format" not in orch
    assert "context_retry" in orch and "miss_log_path" in orch

    with open(BASE_DIR / "data" / "retriever_config.json") as f:
        ret = json.load(f)
    assert "glove_path" not in ret
    assert "vectorization" not in ret


def test_config_ngram_settings_consistent():
    with open(BASE_DIR / "data" / "retriever_config.json") as f:
        cfg = json.load(f)
    assert isinstance(cfg.get("use_char_ngrams", False), bool)
    assert 2 <= cfg.get("char_ngram_n", 3) <= 4