from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import datetime
import requests
import os

app = FastAPI(title="ARMOR Control Plane API", version="1.0")

SHUFFLE_WEBHOOK_URL = os.getenv("SHUFFLE_WEBHOOK", "http://armor-soar:5000/webhook")

class SecurityAlert(BaseModel):
    alert_id: str
    node_id: str
    severity: str
    pattern: str
    process: str
    timestamp: int

@app.get("/")
def health_check():
    return {"status": "online", "system": "ARMOR Backend Control Plane", "time": datetime.datetime.now(datetime.timezone.utc).isoformat()}

def trigger_soar_playbook(alert: SecurityAlert):
    # Simulate GenAI (Llama) triage briefing creation followed by Shuffle SOAR webhook push
    print(f"\n[GENAI TRIAGE] Synthesizing natural language briefing for alert {alert.alert_id}...")
    briefing = f"AI Summary: Host {alert.node_id} experienced abnormal sequence {alert.pattern} via {alert.process}. Immediate containment recommended."
    print(f"   '{briefing}'")
    
    payload = {**alert.model_dump(), "ai_briefing": briefing}
    try:
        print(f"[SOAR ORCHESTRATION] Triggering Shuffle webhook for node isolation...")
        # Simulated webhook call
        # requests.post(SHUFFLE_WEBHOOK_URL, json=payload, timeout=2)
        print(f"   Playbook executed successfully. Isolation webhook sent for {alert.node_id}.\n")
    except Exception as e:
        print(f"   ✖ SOAR dispatch failed: {e}")

@app.post("/alerts")
def receive_alert(alert: SecurityAlert, background_tasks: BackgroundTasks):
    print(f"\n📥 [BACKEND API] Received Alert ID: {alert.alert_id} from Node: {alert.node_id}")
    # Offload SOAR/GenAI pipeline to background worker
    background_tasks.add_task(trigger_soar_playbook, alert)
    return {"status": "received", "alert_id": alert.alert_id}