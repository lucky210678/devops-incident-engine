# agents/remediation_agent.py
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.client import call_llm
from guardrails.output_guard import sanitize_output

def run_remediation_agent(triage_data: dict) -> dict:
    """
    Remediation Agent: Generates fix plans and validates them through output guardrails.
    """
    diagnosis = triage_data.get("diagnosis", "")
    
    prompt = (
        f"You are a DevOps Remediation Agent. Propose a safe step-by-step fix command "
        f"or strategy based on this diagnosis: {diagnosis}"
    )
    
    proposed_fix = call_llm(prompt)
    
    # Run output safety check
    output_guard_result = sanitize_output(proposed_fix)
    
    if not output_guard_result["is_safe"]:
        return {
            "status": "REMEDIATION_BLOCKED",
            "agent": "RemediationAgent",
            "proposed_fix": output_guard_result["sanitized_response"],
            "executed": False
        }
        
    return {
        "status": "RESOLVED",
        "agent": "RemediationAgent",
        "proposed_fix": output_guard_result["sanitized_response"],
        "executed": True
    }