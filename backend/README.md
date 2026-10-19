# ARMOR Backend Control Plane & API

The `backend/` service forms the control plane and API gateway for the **ARMOR Framework**. Built with **FastAPI**, it provides a high-throughput interface for receiving real-time security alerts from the analytics detection engines (Phase 2), storing structured incident records, exposing health/monitoring telemetry, and asynchronously dispatching mitigation requests to GenAI triage and Shuffle SOAR playbooks (Phase 4).

---

## Architecture & Role Breakdown

As part of the **Backend & API Developer** role, this service bridges real-time detection with automated operational response:

1. **Alert Ingestion API:** High-performance REST endpoints to receive structured alert payloads (`/alerts`).
2. **Asynchronous Triage Pipeline:** Uses FastAPI `BackgroundTasks` to offload GenAI briefing generation (via **Ollama / Llama**) and **Shuffle SOAR** playbook webhook execution without blocking incoming HTTP requests.
3. **Time-Series Data Management:** Formatted for direct persistence into **TimescaleDB** for audit logs and historical threat analysis.
4. **Metrics & Health Monitoring:** Exposes system health status and health endpoints ready for **Prometheus** scraping and **Grafana** visualization.

---

## Directory Structure

```text
backend/
├── Dockerfile          # Container build specification for the FastAPI service
├── mock_backend.py     # Main FastAPI application and routing logic
├── README.md           # Backend documentation and API spec
└── requirements.txt    # Python dependencies (FastAPI, Uvicorn, Pydantic, Requests)
