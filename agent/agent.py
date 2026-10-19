import asyncio
import json
import os
import random
import time
from nats.aio.client import Client as NATS

# Configuration from environment variables
NODE_ID = os.getenv("ARMOR_NODE_ID", "edge-node-01")
NATS_URL = os.getenv("ARMOR_NATS_URL", "nats://localhost:4222")
BATCH_SIZE = int(os.getenv("ARMOR_BATCH_SIZE", "5"))
FLUSH_INTERVAL = float(os.getenv("ARMOR_FLUSH_INTERVAL", "2.0"))

async def generate_mock_telemetry():
    """Simulate real-time sensor events (syscalls, network flows)."""
    event_types = ["syscall_execve", "network_conn", "file_access", "priv_escalation"]
    severities = ["INFO", "WARNING", "HIGH", "CRITICAL"]
    
    event = {
        "timestamp": int(time.time() * 1000),
        "node_id": NODE_ID,
        "event_type": random.choice(event_types),
        "severity": random.choice(severities),
        "details": {
            "process": random.choice(["/bin/sh", "/usr/bin/curl", "/usr/sbin/sshd", "nginx"]),
            "pid": random.randint(1000, 65535),
            "remote_ip": f"192.168.1.{random.randint(2, 254)}"
        }
    }
    return event

async def run_agent():
    nc = NATS()
    
    print(f"[{NODE_ID}] Connecting to NATS message bus at {NATS_URL}...")
    while True:
        try:
            await nc.connect(servers=[NATS_URL])
            break
        except Exception as e:
            print(f"[{NODE_ID}] Connection failed: {e}. Retrying in 3 seconds...")
            await asyncio.sleep(3)

    print(f"[{NODE_ID}] Connected successfully. Starting telemetry stream...")
    buffer = []

    try:
        while True:
            event = await generate_mock_telemetry()
            buffer.append(event)
            
            # Flush batch when size is reached
            if len(buffer) >= BATCH_SIZE:
                payload = json.dumps({
                    "batch_id": random.randint(10000, 99999),
                    "node_id": NODE_ID,
                    "count": len(buffer),
                    "events": buffer
                }).encode('utf-8')
                
                subject = f"armor.telemetry.{NODE_ID}"
                await nc.publish(subject, payload)
                print(f"[{NODE_ID}] Published batch of {len(buffer)} events to subject: {subject}")
                
                buffer = []
            
            await asyncio.sleep(FLUSH_INTERVAL)
            
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()
        print(f"[{NODE_ID}] Agent disconnected.")

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("Agent stopped by user.")