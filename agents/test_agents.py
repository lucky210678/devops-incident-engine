# agents/test_agents.py
import sys
import os

# Add project root directory to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.harness import run_incident_loop

if __name__ == "__main__":
    print("Testing Agent Harness, Handoffs, and Execution Loops...\n")
    
    test_incident = "Kubernetes alert: auth-service pod continuously failing with OOMKilled error on IP 10.0.4.12."
    
    final_state = run_incident_loop(test_incident)
    print("\n" + "="*60)
    print("Final State Summary:")
    print(f"Status: {final_state.get('status')}")
    print("="*60)