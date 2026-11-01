# agents/harness.py
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from agents.triage_agent import run_triage_agent
from agents.remediation_agent import run_remediation_agent

def run_incident_loop(incident_alert: str, max_loops: int = 3) -> dict:
    """
    Agent Harness: Controls state transitions, handoffs, and loop limits.
    """
    print(f"--- [Harness] Starting Incident Loop (Max Loops: {max_loops}) ---")
    
    loop_count = 0
    state = {"alert": incident_alert, "status": "STARTING"}
    
    while loop_count < max_loops:
        loop_count += 1
        print(f"\n[Loop Execution #{loop_count}]")
        
        # Step 1: Triage Phase
        triage_result = run_triage_agent(state["alert"])
        state.update(triage_result)  # Preserve triage state and diagnosis
        
        print(f"-> Triage Status: {triage_result['status']}")
        print(f"-> Diagnosis:     {triage_result['diagnosis']}")
        
        if triage_result["status"] == "BLOCKED":
            break
            
        # Step 2: Handoff to Remediation Agent
        if triage_result.get("needs_remediation"):
            print("-> [Handoff] Delegating from TriageAgent to RemediationAgent...")
            remediation_result = run_remediation_agent(triage_result)
            print(f"-> Remediation Status: {remediation_result['status']}")
            print(f"-> Fix Plan:           {remediation_result['proposed_fix']}")
            
            state.update(remediation_result)
            if remediation_result["status"] in ["RESOLVED", "REMEDIATION_BLOCKED"]:
                break
                
    return state