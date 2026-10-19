# ARMOR: Autonomous Research for Monitoring and Operational Response

**ARMOR** is an early-stage research project dedicated to developing a distributed, autonomous cyber defense framework. The goal of ARMOR is to move beyond reactive security by creating a system that can independently monitor heterogeneous client systems, detect emerging threats in real-time, and provide a centralized orchestration layer for rapid mitigation.

## Project Vision
Modern networks are too large and complex for manual monitoring. ARMOR is being designed to solve the "visibility gap" by deploying lightweight, autonomous agents that act as a collective immune system for distributed infrastructure.



## Core Research Pillars

### 1. Distributed Autonomous Telemetry
ARMOR implements a novel distributed architecture designed to automate the collection and monitoring of heterogeneous client systems in real-time. 
* **The Problem:** Centralized logging often creates network bottlenecks and single points of failure in large-scale environments.
* **The ARMOR Approach:** We are engineering a lightweight, agent-based architecture that enables autonomous telemetry collection at the edge.
* **Objective:** To maintain total systemic visibility across disparate distributed environments without compromising network performance or increasing latency.

### 2. Autonomous Threat & Vulnerability Detection
To combat the rise of zero-day exploits and sophisticated lateral movement, ARMOR integrates autonomous detection engines directly into its distributed nodes.
* **The Problem:** Traditional signature-based detection is reactive and fails against previously unknown threats.
* **The ARMOR Approach:** By implementing Apache Flink Complex Event Processing (CEP) and GraphSAGE Graph Neural Networks (GNN), the system is designed to independently identify anomalous system states and vulnerabilities.
* **Objective:** To shift the defense paradigm from reactive patching to proactive, autonomous discovery of threats before they can be exploited.

### 3. Situational Awareness & Mitigation Orchestration
Data is only useful if it is actionable. ARMOR features a comprehensive visualization dashboard that translates complex distributed telemetry into high-level intelligence.
* **The Problem:** Security analysts are often overwhelmed by "alert fatigue" and fragmented toolsets during a breach.
* **The ARMOR Approach:** A "single pane of glass" interface that combines real-time visualization with a mitigation orchestration layer via Shuffle SOAR. This allows administrators to deploy countermeasures across the entire distributed network instantly.
* **Objective:** To enhance Cyber Situational Awareness (CSA) and significantly reduce the Mean Time to Remediate (MTTR) by reducing cognitive load on the operator.


## Roadmap & Current Status
**Status: Initial Research / Alpha Phase**

- **Phase 1:** Development of the lightweight telemetry agent & NATS bus transport.
- **Phase 2:** Implementation of basic anomaly detection algorithms (Flink CEP).
- **Phase 3:** Integration of structural graph analytics (GraphSAGE GNN).
- **Phase 4:** Beta release of the Visualization & Mitigation Dashboard (Shuffle SOAR & Grafana).

Here is a comprehensive **To-Do List** to track your progress as you build, test, and deploy the **ARMOR Framework** across all phases, roles, and open-source components.


# ARMOR Framework Development To-Do List

### Phase 1: Distributed Autonomous Telemetry

*Focus: Edge sensing, agent wrappers, and low-latency message transport.*

* [x] Create core edge agent script (`agent/agent.py`) for mock syscall and network event streaming.
* [x] Configure agent containerization (`agent/Dockerfile` and `agent/requirements.txt`).
* [x] Set up central NATS message broker service in `docker-compose.yml`.
* [x] Write agent scaling script (`scripts/scale-agents.sh`) to spin up multiple concurrent nodes.
* [ ] Integrate real **Falco** or **Zeek** rules into the edge agent container for production sensor data.

### Phase 2: Algorithmic Detection & Graph Analytics

*Focus: Stateful complex event processing (CEP) and graph neural networks.*

* [x] Implement sliding-window CEP sequence matching (`analytics/mock_analytics.py`).
* [x] Implement network topology graphing via NetworkX / PyG placeholders.
* [x] Configure analytics service containerization and link it to the NATS telemetry stream.
* [ ] Replace mock NetworkX topology with a live **Neo4j** graph database connection.
* [ ] Train an initial inductive node-embedding model using **PyTorch Geometric (PyG)**.

### Phase 3: Backend Control Plane & API

*Focus: FastAPI web server, time-series data storage, and control plane endpoints.*

* [x] Build FastAPI backend endpoints (`backend/mock_backend.py`) for incoming security alerts.
* [x] Configure backend containerization and expose ports (`backend/Dockerfile`).
* [ ] Connect FastAPI persistence layer to **TimescaleDB** for long-term audit logging.
* [ ] Expose **Prometheus** metrics endpoint on the backend for infrastructure monitoring.

### Phase 4: GenAI & Orchestration (SOAR)

*Focus: Automated threat briefings and closed-loop mitigation hooks.*

* [x] Implement automated GenAI triage briefing simulator (Llama prompt structure).
* [x] Setup asynchronous background worker trigger for SOAR webhooks.
* [ ] Connect local **Ollama + Llama** container service for live LLM response generation.
* [ ] Deploy active **Shuffle SOAR** instance via Docker to execute real webhook playbooks.

### Phase 5: Dashboard, DevOps & Cloud Deployment

*Focus: Visualization UI, CI/CD pipelines, and cloud migration.*

* [x] Build single-file interactive system architecture presentation (`web/index.html`).
* [ ] Configure **Grafana Loki** dashboard container for log aggregation and visualization.
* [ ] Write GitHub Actions workflow (`.github/workflows/ci-cd.yml`) for automated testing and builds.
* [ ] Prepare infrastructure provisioning scripts for **AWS EC2** or **GCP Cloud Run**.
