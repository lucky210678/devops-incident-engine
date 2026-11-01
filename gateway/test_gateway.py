# gateway/test_gateway.py
import sys
import os

# Automatically add the gateway folder to Python's search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import call_llm
from router import route_task

if __name__ == "__main__":
    print("Testing Smart Router & LLM Gateway Pipeline...\n")
    
    sample_alerts = [
        "Summarize the daily deployment status for the frontend pod.",
        "CRITICAL: Production DB connection pool exhausted. Perform root cause analysis."
    ]
    
    for alert in sample_alerts:
        selected_model = route_task(alert)
        print(f"Alert: '{alert}'")
        print(f"-> Selected Model Route: {selected_model}")
        
        response = call_llm(prompt=alert, model_name=selected_model)
        print(f"-> Gateway Response: {response}\n" + "-"*60)