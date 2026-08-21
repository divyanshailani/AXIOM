import json
import sys
from pathlib import Path

from axiom.orchestrator import AxiomOrchestrator

BASE_DIR = Path(__file__).parent

# Golden routing expectations for the 51 test prompts. Each entry maps a prompt
# (or a substring match) to the domain it MUST route to. Prompts not listed are
# evaluated against the story rules below instead.
GOLDEN_DOMAINS = {
    "hey": "chit_chat",
    "hello": "chit_chat",
    "good morning": "chit_chat",
    "how are you": "chit_chat",
    "who are you": "chit_chat",
    "what is your name": "chit_chat",
    "are you a robot": "chit_chat",
    "what can you do": "chit_chat",
    "tell me a joke": "chit_chat",
    "bye": "chit_chat",
    # classical ML
    "what is machine learning": "classical_ml",
    "explain classical ml": "classical_ml",
    "what is artificial intelligence": "classical_ml",
    "maths": "classical_ml",
    "algorithms": "classical_ml",
    "data science": "classical_ml",
    "what is linear regression": "classical_ml",
    "how does regression work": "classical_ml",
    "explain ordinary least squares": "classical_ml",
    "what is logistic regression": "classical_ml",
    "explain logistic regression": "classical_ml",
    "how does the sigmoid function work": "classical_ml",
    "what are decision trees": "classical_ml",
    "how do decision trees work": "classical_ml",
    "explain random forests": "classical_ml",
    "what is entropy in a decision tree": "classical_ml",
    "whats xgboost": "classical_ml",
    "what is a support vector machine": "classical_ml",
    "explain svm": "classical_ml",
    "what is a kernel trick": "classical_ml",
    "how does svm classify": "classical_ml",
    "what is clustering": "classical_ml",
    "explain k means clustering": "classical_ml",
    "what is unsupervised learning": "classical_ml",
    "how does k means work": "classical_ml",
    "what is k nearest neighbors": "classical_ml",
    "explain knn": "classical_ml",
    "how does nearest neighbor work": "classical_ml",
    # self
    "how do you understand my questions": "self",
    "what is cosine similarity": "self",
    "how do you generate sentences": "self",
    "what is a markov chain": "self",
    "how do you pick a domain": "self",
    "what is naive bayes": "self",
    "how do you work": "self",
    # history
    "who invented the perceptron": "history",
    "who is alan turing": "history",
    "what is the turing test": "history",
    # modern context
    "what are transformers": "modern_context",
    "how does chatgpt work": "modern_context",
    "why are you not a neural network": "modern_context",
}


def classify(prompt: str, resp) -> tuple:
    """Return (passed: bool, reason: str) for a single prompt's result."""
    if resp.intent_id == "unknown":
        return False, f"unknown intent (sim {resp.similarity_score:.2f})"
    if resp.similarity_score <= 0.0:
        return False, "zero similarity score"
    expected = GOLDEN_DOMAINS.get(prompt.strip().lower())
    if expected and resp.domain != expected:
        return False, f"routed to {resp.domain}, expected {expected}"
    return True, f"{resp.domain}/{resp.intent_id} ({resp.similarity_score:.2f})"


def main():
    print("Initializing AXIOM Orchestrator...")
    orchestrator = AxiomOrchestrator()
    
    with open(BASE_DIR / "test_cases.json", "r") as f:
        prompts = json.load(f)
        
    print(f"Running {len(prompts)} test cases...\n")
    
    failures = []
    with open(BASE_DIR / "test_results.md", "w") as out:
        out.write("# AXIOM Test Results\n\n")
        out.write(f"This file contains the output of {len(prompts)} test prompts (general & technical) run against the Zero-Training math engines.\n\n")
        
        for i, prompt in enumerate(prompts):
            response = orchestrator.chat(prompt)
            passed, reason = classify(prompt, response)
            status = "PASS" if passed else "FAIL"
            if not passed:
                failures.append((i + 1, prompt, reason))
            
            out.write(f"### Test {i+1}: `{prompt}` — **{status}**\n")
            out.write(f"- **Domain Route**: `{response.domain}` (Confidence: {response.domain_confidence:.2%})\n")
            out.write(f"- **Intent Match**: `{response.intent_id}` (Sim Score: {response.similarity_score:.2f})\n")
            out.write(f"- **Routing Check**: {reason}\n")
            out.write(f"- **AXIOM Response**: {response.response_text}\n\n")
            
    print(f"Testing complete. Results saved to test_results.md")
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for idx, prompt, reason in failures:
            print(f"  #{idx} {prompt!r}: {reason}")
        sys.exit(1)
    print("All test cases passed the routing checks.")


if __name__ == "__main__":
    main()