import sys
from axiom.orchestrator import AxiomOrchestrator

def main():
    print("="*60)
    print("AXIOM: Zero-Training Classical ML Chatbot (CLI Test Mode)")
    print("Type 'quit' or 'exit' to stop.")
    print("="*60)
    
    try:
        orchestrator = AxiomOrchestrator()
        print("Pipeline initialized instantly (Zero-Training!).\n")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return
        
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit']:
                break
                
            response = orchestrator.chat(user_input)
            
            print(f"\nAXIOM: {response.response_text}")
            print(f"  [Math Engine -> Domain: '{response.domain}' ({response.domain_confidence:.2%}) | "
                  f"Intent: '{response.intent_id}' (Sim Score: {response.similarity_score:.2f})]\n")
                  
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            
    print("\nShutting down AXIOM.")

if __name__ == "__main__":
    main()
