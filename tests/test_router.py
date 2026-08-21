from axiom.core.router import NaiveBayesRouter


def test_router_self_domain(loaded_memory, router_config):
    router = NaiveBayesRouter(loaded_memory, router_config)
    probs = router.predict_proba("yourself")

    assert probs['self'] > probs['classical_ml'], f"Expected self to win over classical_ml, got {probs}"
    assert probs['self'] > probs['history'], f"Expected self to win over history, got {probs}"


def test_router_modern_context_for_transformers(loaded_memory, router_config):
    router = NaiveBayesRouter(loaded_memory, router_config)
    probs = router.predict_proba("what are transformers")

    assert probs['modern_context'] > probs['chit_chat'], (
        f"transformers should route to modern_context, got {probs}"
    )


def test_router_probabilities_sum_to_one(loaded_memory, router_config):
    router = NaiveBayesRouter(loaded_memory, router_config)
    probs = router.predict_proba("hello")

    assert abs(sum(probs.values()) - 1.0) < 1e-9


def test_router_handles_contraction_and_typo_variants(loaded_memory, router_config):
    router = NaiveBayesRouter(loaded_memory, router_config)
    # 'what's' / 'whats' should end up the same token; 'svm' vs 'svms' fold together.
    # 'what' itself is a stopword so it is filtered out of the token stream.
    tokens = router._tokenize("what's svm svms")
    assert "svm" in tokens, f"expected svm token, got {tokens}"
    assert "what" not in tokens, f"'what' is a stopword and must be filtered, got {tokens}"


def test_router_rejects_empty_query_with_graceful_response(loaded_memory, router_config):
    router = NaiveBayesRouter(loaded_memory, router_config)
    probs = router.predict_proba("")
    # Should not crash; returns the prior distribution.
    assert abs(sum(probs.values()) - 1.0) < 1e-9