import pytest
from pathlib import Path
from axiom.core.router import NaiveBayesRouter

def test_router_self_domain():
    base_dir = Path(__file__).parent.parent
    router = NaiveBayesRouter(
        base_dir / "data" / "memory.json",
        base_dir / "data" / "router_config.json"
    )
    probs = router.predict_proba("yourself")
    
    assert probs['self'] > probs['classical_ml'], f"Expected self to win over classical_ml, got {probs}"
    assert probs['self'] > probs['history'], f"Expected self to win over history, got {probs}"
