# ARMOR Automation Scripts

This directory contains utility and deployment automation scripts for setting up, building, and running the ARMOR framework components.

To deploy and scale multiple telemetry agents in the ARMOR framework, you can use automated scripting to spin up multiple edge nodes dynamically. Each agent connects to the central NATS messaging bus while operating independently with its own unique Node ID (`edge-node-03`, `edge-node-04`, etc.).

`scale-agents.sh`, designed to scale your edge telemetry fleet on-demand.


### How to Use the Scaling Script

1. Make the script executable (if not already done):
```bash
chmod +x scripts/scale-agents.sh
```

2. Run the script and specify how many agents you want to deploy (e.g., scale up to **10 concurrent edge nodes**):
```bash
./scripts/scale-agents.sh 10
```


3. Verify that all agents are successfully streaming telemetry into the central NATS bus:
```bash
docker ps --filter "name=armor-agent"
```