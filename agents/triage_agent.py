# agents/triage_agent.py
import sys
import os

# Insert project root directory at priority 0 in Python's search path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.client import call_llm
from guardrails.input_guard import sanitize_input
from tools.kubectl_simulator import get_pod_logs
from tools.db_diagnostics import get_db_metrics

def run_triage_agent(incident_alert: str) -> dict:
    """
    Triage Agent: Validates input safety, gathers diagnostic data, and diagnoses the incident.
    """
    # 1. Apply Input Guardrail
    guard_result = sanitize_input(incident_alert)
    if not guard_result["is_safe"]:
        return {
            "status": "BLOCKED",
            "agent": "TriageAgent",
            "diagnosis": guard_result["reason"],
            "needs_remediation": False
        }
    
    clean_alert = guard_result["sanitized_prompt"]
    
    # 2. Collect tool diagnostics based on alert context
    diagnostics = ""
    if "pod" in clean_alert.lower() or "k8s" in clean_alert.lower():
        diagnostics = get_pod_logs("auth-service-pod")
    elif "db" in clean_alert.lower() or "database" in clean_alert.lower():
        diagnostics = get_db_metrics("prod-db-01")
    else:
        diagnostics = "No specialized diagnostic tool required."
        
    # 3. Construct prompt for LLM analysis
    prompt = (
        f"You are a DevOps Triage Agent. Analyze this alert and diagnostic data:\n"
        f"Alert: {clean_alert}\n"
        f"Diagnostics: {diagnostics}\n"
        f"Provide a 1-sentence root cause diagnosis."
    )
    
    diagnosis_response = call_llm(prompt)
    
    return {
        "status": "TRIAGED",
        "agent": "TriageAgent",
        "clean_alert": clean_alert,
        "diagnostics": diagnostics,
        "diagnosis": diagnosis_response,
        "needs_remediation": True
    }