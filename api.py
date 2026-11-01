# api.py
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Ensure project root directory is prioritized in Python search path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.router import route_task
from guardrails.input_guard import sanitize_input
from agents.harness import run_incident_loop

app = FastAPI(
    title="DevOps Incident Response Copilot API",
    description="Autonomous multi-agent LLM pipeline with guardrails, smart routing, and resilient fallbacks.",
    version="1.0.0"
)

class IncidentRequest(BaseModel):
    alert: str

class IncidentResponse(BaseModel):
    status: str
    router_target: str
    sanitized_alert: str
    diagnosis: str | None = None
    proposed_fix: str | None = None

@app.get("/")
def health_check():
    return {"status": "ONLINE", "service": "DevOps Incident Response Copilot"}

@app.post("/incident", response_model=IncidentResponse)
def process_incident(request: IncidentRequest):
    if not request.alert.strip():
        raise HTTPException(status_code=400, detail="Alert payload cannot be empty.")
    
    # 1. Smart Routing
    target_model = route_task(request.alert)
    
    # 2. Input Guardrails
    guard_check = sanitize_input(request.alert)
    if not guard_check["is_safe"]:
        return IncidentResponse(
            status="BLOCKED",
            router_target=target_model,
            sanitized_alert=request.alert,
            diagnosis=guard_check["reason"],
            proposed_fix=None
        )
    
    # 3. Multi-Agent Control Harness Execution
    final_state = run_incident_loop(guard_check["sanitized_prompt"])
    
    return IncidentResponse(
        status=final_state.get("status", "UNKNOWN"),
        router_target=target_model,
        sanitized_alert=guard_check["sanitized_prompt"],
        diagnosis=final_state.get("diagnosis"),
        proposed_fix=final_state.get("proposed_fix")
    )