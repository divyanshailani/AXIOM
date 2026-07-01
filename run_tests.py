import json
from axiom.orchestrator import AxiomOrchestrator

def main():
    print("Initializing AXIOM Orchestrator...")
    orchestrator = AxiomOrchestrator()
    
    with open("test_cases.json", "r") as f:
        prompts = json.load(f)
        
    print(f"Running {len(prompts)} test cases...\n")
    
    with open("test_results.md", "w") as out:
        out.write("# AXIOM V1 Test Results\n\n")
        out.write("This file contains the output of 50 test prompts (general & technical) run against the V1 Zero-Training math engines.\n\n")
        
        for i, prompt in enumerate(prompts):
            response = orchestrator.chat(prompt)
            
            out.write(f"### Test {i+1}: `{prompt}`\n")
            out.write(f"- **Domain Route**: `{response.domain}` (Confidence: {response.domain_confidence:.2%})\n")
            out.write(f"- **Intent Match**: `{response.intent_id}` (Sim Score: {response.similarity_score:.2f})\n")
            out.write(f"- **AXIOM Response**: {response.response_text}\n\n")
            
    print("Testing complete. Results saved to test_results.md")

if __name__ == "__main__":
    main()
