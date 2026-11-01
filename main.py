# main.py
import sys
import os

# Ensure project root directory is prioritized in Python search path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.router import route_task
from guardrails.input_guard import sanitize_input
from agents.harness import run_incident_loop

def run_copilot(alert_text: str):
    print("\n" + "="*70)
    print("🚨 DEVOPS INCIDENT RESPONSE COPILOT DETECTED NEW ALERT")
    print("="*70)
    print(f"Raw Alert: {alert_text}")

    # 1. Smart Routing
    suggested_model = route_task(alert_text)
    print(f"-> Router Target: {suggested_model}")

    # 2. Input Guardrail Verification
    guard_check = sanitize_input(alert_text)
    if not guard_check["is_safe"]:
        print(f"❌ Alert Rejected by Guardrail: {guard_check['reason']}")
        return

    print(f"-> Guardrail Sanitized Alert: {guard_check['sanitized_prompt']}")

    # 3. Multi-Agent Execution Loop (Triage -> Handoff -> Remediation)
    final_state = run_incident_loop(guard_check["sanitized_prompt"])

    # 4. Final Executive Summary
    print("\n" + "="*70)
    print("📊 INCIDENT RESOLUTION REPORT")
    print("="*70)
    print(f"Status:       {final_state.get('status')}")
    print(f"Diagnosis:    {final_state.get('diagnosis')}")
    print(f"Fix Strategy: {final_state.get('proposed_fix')}")
    print("="*70 + "\n")

if __name__ == "__main__":
    print("Initializing DevOps Incident Response Copilot Pipeline...\n")
    
    # Test Incident 1: Kubernetes Pod OOM Error
    k8s_alert = "Kubernetes alert: auth-service-pod continuously failing with OOMKilled error on IP 10.0.4.12 using key gsk_1234567890abcdef."
    run_copilot(k8s_alert)

    # Test Incident 2: Database Connection Exhaustion
    db_alert = "CRITICAL DB alert: prod-db-01 connection pool exhausted with high query queue latency."
    run_copilot(db_alert)