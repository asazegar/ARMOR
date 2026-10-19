#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting ARMOR Framework Deployment (Phase 1)..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker to proceed."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not available. Please install Docker Compose v2."
    exit 1
fi

echo "📦 Building edge agent images and starting NATS messaging bus..."
docker compose up --build -d

echo "ARMOR Phase 1 telemetry environment is successfully running!"
echo ""
echo "💡 Useful commands:"
echo "   - View logs:    docker compose logs -f"
echo "   - Stop cluster: docker compose down"