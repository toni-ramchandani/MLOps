#!/bin/bash
# Validation script for Docker Compose and API health checks

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$script_dir/docker-compose.yml"
API_URL="http://localhost:8000"
HEALTH_ENDPOINT="/docs"  # FastAPI's Swagger UI
MAX_RETRIES=30
RETRY_DELAY=1

echo "🚀 Starting validation..."

# Step 1: Start Docker Compose
echo "\n📦 Starting Docker Compose services..."
docker compose -f "$COMPOSE_FILE" up -d --build

# Step 2: Check running containers
echo "\n✅ Checking running containers..."
docker compose -f "$COMPOSE_FILE" ps

# Step 3: Wait for API to be ready
echo "\n⏳ Waiting for API to be ready..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s "$API_URL$HEALTH_ENDPOINT" > /dev/null; then
        echo "✓ API is ready!"
        break
    fi
    if [ $i -eq $MAX_RETRIES ]; then
        echo "✗ API failed to start after $MAX_RETRIES attempts"
        docker compose -f "$COMPOSE_FILE" logs api
        exit 1
    fi
    echo "  Attempt $i/$MAX_RETRIES..."
    sleep $RETRY_DELAY
done

# Step 4: Test API endpoints
echo "\n🧪 Testing API endpoints..."

# Test health check (if exists)
if curl -s "$API_URL/health" > /dev/null 2>&1; then
    echo "✓ GET /health - OK"
else
    echo "⚠ GET /health - Not found (optional)"
fi

# Test docs endpoint
if curl -s "$API_URL/docs" > /dev/null; then
    echo "✓ GET /docs - OK"
fi

# Step 5: Check service logs
echo "\n📋 Service logs (last 10 lines):"
echo "--- API ---"
docker compose -f "$COMPOSE_FILE" logs --tail=10 api

echo "\n✨ Validation complete! Your stack is running."
echo "API available at: $API_URL"
echo "Documentation at: $API_URL/docs"
echo "\nTo stop services: docker compose -f $COMPOSE_FILE down"
