import pytest
from pathlib import Path
from axiom.core.retriever import IntentRetriever

def test_retriever_svm_intent():
    base_dir = Path(__file__).parent.parent
    retriever = IntentRetriever(
        base_dir / "data" / "memory.json",
        base_dir / "data" / "retriever_config.json",
        domain='classical_ml'
    )
    
    intent, score = retriever.find_intent("explain support vector machines")
    assert intent == 'ml_svm', f"Expected ml_svm, got {intent}"
    assert score > 0.4, f"Expected score > 0.4, got {score}"

def test_retriever_unknown_intent():
    base_dir = Path(__file__).parent.parent
    retriever = IntentRetriever(
        base_dir / "data" / "memory.json",
        base_dir / "data" / "retriever_config.json",
        domain='classical_ml'
    )
    
    intent, score = retriever.find_intent("how to bake a cake")
    assert intent == 'unknown', f"Expected unknown, got {intent}"
    assert score < 0.25, f"Expected score < 0.25, got {score}"
