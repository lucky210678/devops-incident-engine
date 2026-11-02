# api.py
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.router import route_task
from guardrails.input_guard import sanitize_input
from agents.harness import run_incident_loop
from database import init_db, save_incident, get_all_incidents, get_incident_by_id

# Initialize SQLite database on startup
init_db()

app = FastAPI(
    title="DevOps Incident Response Engine API",
    description="Autonomous incident response platform with SQLite session history.",
    version="1.0.0"
)

class IncidentRequest(BaseModel):
    alert: str

class IncidentResponse(BaseModel):
    id: int
    status: str
    router_target: str
    sanitized_alert: str
    diagnosis: str | None = None
    proposed_fix: str | None = None

@app.get("/")
def health_check():
    return {"status": "ONLINE", "service": "DevOps Incident Response Engine"}

@app.post("/incident", response_model=IncidentResponse)
def process_incident(request: IncidentRequest):
    if not request.alert.strip():
        raise HTTPException(status_code=400, detail="Alert payload cannot be empty.")
    
    target_model = route_task(request.alert)
    guard_check = sanitize_input(request.alert)
    
    if not guard_check["is_safe"]:
        incident_id = save_incident(
            sanitized_alert=request.alert,
            status="BLOCKED",
            diagnosis=guard_check["reason"],
            proposed_fix=None
        )
        return IncidentResponse(
            id=incident_id,
            status="BLOCKED",
            router_target=target_model,
            sanitized_alert=request.alert,
            diagnosis=guard_check["reason"],
            proposed_fix=None
        )
    
    final_state = run_incident_loop(guard_check["sanitized_prompt"])
    
    # Save processed result into SQLite
    incident_id = save_incident(
        sanitized_alert=guard_check["sanitized_prompt"],
        status=final_state.get("status", "UNKNOWN"),
        diagnosis=final_state.get("diagnosis"),
        proposed_fix=final_state.get("proposed_fix")
    )
    
    return IncidentResponse(
        id=incident_id,
        status=final_state.get("status", "UNKNOWN"),
        router_target=target_model,
        sanitized_alert=guard_check["sanitized_prompt"],
        diagnosis=final_state.get("diagnosis"),
        proposed_fix=final_state.get("proposed_fix")
    )

# ------------------------------------------------------------------
# HISTORY ENDPOINTS (Populates Gemini-style sidebar)
# ------------------------------------------------------------------

@app.get("/incidents/history")
def get_history_sidebar():
    """Returns a list of all past incidents to populate a sidebar."""
    return get_all_incidents()

@app.get("/incidents/{incident_id}")
def get_incident_detail(incident_id: int):
    """Fetches full log and diagnosis when a user selects a history item."""
    incident = get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident session not found.")
    return incident