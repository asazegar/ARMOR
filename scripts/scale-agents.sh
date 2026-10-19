#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Default to 5 agents if no argument is provided
TARGET_COUNT=${1:-5}

echo "Scaling ARMOR telemetry edge agents to $TARGET_COUNT instances..."

# 1. Ensure the NATS message bus is running
if ! docker ps --format '{{.Names}}' | grep -q "armor-nats-bus"; then
    echo "⚠️ Central NATS bus is not running. Starting base infrastructure..."
    docker compose up -d nats-bus
fi

# 2. Ensure the agent image is built
echo "Ensuring agent image is built..."
docker compose build armor-agent-01 > /dev/null 2>&1 || docker build -t armor-agent:latest ./agent

# Find the correct docker network created by docker compose
NETWORK_NAME=$(docker network ls --format '{{.Name}}' | grep -E 'armor.*default' | head -n 1)
if [ -z "$NETWORK_NAME" ]; then
    NETWORK_NAME="armor-framework_default"
fi

# 3. Loop and deploy agents starting from index 3 up to TARGET_COUNT
for ((i=1; i<=TARGET_COUNT; i++)); do
    NODE_ID=$(printf "edge-node-%02d" $i)
    CONTAINER_NAME="armor-agent-$i"

    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        echo "Container $CONTAINER_NAME already exists. Restarting..."
        docker start "$CONTAINER_NAME" > /dev/null 2>&1
    else
        echo "✨ Spawning $CONTAINER_NAME ($NODE_ID)..."
        docker run -d \
            --name "$CONTAINER_NAME" \
            --network "$NETWORK_NAME" \
            -e ARMOR_NODE_ID="$NODE_ID" \
            -e ARMOR_NATS_URL="nats://armor-nats-bus:4222" \
            -e ARMOR_BATCH_SIZE=5 \
            -e ARMOR_FLUSH_INTERVAL=2.0 \
            armor-framework-armor-agent-01:latest > /dev/null 2>&1
    fi
done

echo ""
echo "Successfully scaled! Total active edge agents: $TARGET_COUNT"
echo "Run 'docker stats' to monitor resource usage or 'docker compose logs -f' to view streams."