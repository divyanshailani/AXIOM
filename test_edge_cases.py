import sys
from axiom.orchestrator import AxiomOrchestrator

orchestrator = AxiomOrchestrator()
prompts = [
    "& what's DL ?",
    "i see",
    "explain your architecture",
    "binary cross entropy ?",
    "AUC & ROC ?",
    "you were wrong"
]

for p in prompts:
    resp = orchestrator.chat(p)
    print(f"Prompt: '{p}'")
    print(f"  Domain: {resp.domain} ({resp.domain_confidence:.2f})")
    print(f"  Intent: {resp.intent_id} ({resp.similarity_score:.2f})")
    pass
    print("-" * 40)
