import asyncio
import json
import os
import time
from collections import defaultdict, deque
from nats.aio.client import Client as NATS
import networkx as nx

NATS_URL = os.getenv("ARMOR_NATS_URL", "nats://nats-bus:4222")

# Stateful sliding window tracking for CEP (e.g., rapid command execution after file access)
event_windows = defaultdict(lambda: deque(maxlen=10))

# Graph topology model for structural anomaly detection
topology_graph = nx.DiGraph()

async def process_telemetry_message(msg):
    try:
        data = json.loads(msg.data.decode('utf-8'))
        batch_id = data.get("batch_id")
        node_id = data.get("node_id")
        events = data.get("events", [])

        print(f"[ANALYTICS] Received batch {batch_id} from {node_id} ({len(events)} events)")

        for ev in events:
            ev_type = ev.get("event_type")
            severity = ev.get("severity")
            details = ev.get("details", {})
            process = details.get("process")
            remote_ip = details.get("remote_ip")

            # --- 1. Graph Topology Update (Structural Analysis) ---
            topology_graph.add_node(node_id, type="host")
            if remote_ip:
                topology_graph.add_node(remote_ip, type="external_ip")
                topology_graph.add_edge(node_id, remote_ip, action=ev_type)

            # --- 2. Complex Event Processing (CEP) Sequence Matching ---
            window = event_windows[node_id]
            window.append({
                "type": ev_type,
                "process": process,
                "time": time.time()
            })

            # Check sequence rule: File access followed rapidly by shell execution / privilege escalation
            if len(window) >= 2:
                recent_events = list(window)
                last_two = [e['type'] for e in recent_events[-2:]]
                
                if last_two == ["file_access", "priv_escalation"] or last_two == ["syscall_execve", "priv_escalation"]:
                    print(f"\n[CEP ALERT] Multi-stage attack sequence detected on node: {node_id}!")
                    print(f"   Pattern matched: {last_two} via process {process}")
                    print(f"   Action: Triggering automated mitigation signal...\n")

            # Simple Graph-based degree anomaly check (simulating GraphSAGE neighbor analysis)
            if node_id in topology_graph:
                degree = topology_graph.degree(node_id)
                if degree > 15:
                    print(f"[GRAPH ANOMALY] Node {node_id} exhibits high connectivity degree ({degree}). Potential lateral movement.")

    except Exception as e:
        print(f"[ANALYTICS] Error processing message: {e}")

async def run_detection_engine():
    nc = NATS()
    print(f"[ANALYTICS] Connecting to NATS message bus at {NATS_URL}...")
    
    while True:
        try:
            await nc.connect(servers=[NATS_URL])
            break
        except Exception as e:
            print(f"[ANALYTICS] Connection failed: {e}. Retrying in 3s...")
            await asyncio.sleep(3)

    print("[ANALYTICS] Connected! Subscribing to telemetry subject wildcard 'armor.telemetry.*'...")
    await nc.subscribe("armor.telemetry.*", cb=process_telemetry_message)

    # Keep engine alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_detection_engine())
    except KeyboardInterrupt:
        print("Detection engine stopped.")