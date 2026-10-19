import asyncio
import json
import os
import random
import time
from collections import defaultdict, deque
from nats.aio.client import Client as NATS
import networkx as nx
import requests

NATS_URL = os.getenv("ARMOR_NATS_URL", "nats://nats-bus:4222")
BACKEND_API_URL = os.getenv("ARMOR_BACKEND_URL", "http://armor-backend:8000/alerts")

event_windows = defaultdict(lambda: deque(maxlen=10))
topology_graph = nx.DiGraph()

async def process_telemetry(msg):
    try:
        data = json.loads(msg.data.decode('utf-8'))
        node_id = data.get("node_id")
        events = data.get("events", [])

        print(f"[ANALYTICS] Processing telemetry batch from {node_id} ({len(events)} events)")

        for ev in events:
            ev_type = ev.get("event_type")
            details = ev.get("details", {})
            process = details.get("process")
            remote_ip = details.get("remote_ip")

            # 1. Update Graph Topology (Mock GraphSAGE / NetworkX)
            topology_graph.add_node(node_id, type="host")
            if remote_ip:
                topology_graph.add_node(remote_ip, type="external_ip")
                topology_graph.add_edge(node_id, remote_ip, action=ev_type)

            # 2. Stateful CEP Sliding Window Check
            window = event_windows[node_id]
            window.append({"type": ev_type, "process": process})

            if len(window) >= 2:
                last_two = [e['type'] for e in list(window)[-2:]]
                # Trigger mock alert on suspicious pattern
                if last_two == ["file_access", "priv_escalation"] or random.random() < 0.2:
                    alert_payload = {
                        "alert_id": f"ALT-{random.randint(10000, 99999)}",
                        "node_id": node_id,
                        "severity": "CRITICAL",
                        "pattern": str(last_two),
                        "process": process,
                        "timestamp": int(time.time())
                    }
                    print(f"\n🚨 [CEP / GNN ALERT DETECTED] Node: {node_id} | Pattern: {last_two}")
                    
                    # Forward alert to Backend & SOAR orchestration
                    try:
                        requests.post(BACKEND_API_URL, json=alert_payload, timeout=2)
                        print(f"   ➔ Dispatched alert to Backend API.")
                    except Exception as req_err:
                        print(f"   ✖ Failed to notify backend: {req_err}")

    except Exception as e:
        print(f"[ANALYTICS] Error: {e}")

async def main():
    nc = NATS()
    print(f"[ANALYTICS] Connecting to NATS at {NATS_URL}...")
    while True:
        try:
            await nc.connect(servers=[NATS_URL])
            break
        except:
            await asyncio.sleep(3)

    print("[ANALYTICS] Subscribed to telemetry feeds.")
    await nc.subscribe("armor.telemetry.*", cb=process_telemetry)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())