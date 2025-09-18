#!/bin/bash
set -euo pipefail

# FastAPI vs Django Performance Benchmark Startup Script (Incremental)

echo "🚀 Starting FastAPI vs Django Performance Benchmark"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create results directory
mkdir -p results

# Build and start services
echo "📦 Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 35

# Check if services are running
echo "🔍 Checking service health..."

# Check FastAPI
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ FastAPI is running on http://localhost:8000"
else
    echo "❌ FastAPI is not responding"
    exit 1
fi

# Check Django
if curl -s http://localhost:8001/api/benchmark/health/ > /dev/null; then
    echo "✅ Django is running on http://localhost:8001"
else
    echo "❌ Django is not responding"
    exit 1
fi

# Apply Django migrations
echo "🛠️ Applying Django migrations..."
docker-compose exec -T django python manage.py migrate --noinput

# Ensure Python venv exists and install dependencies
echo "📋 Ensuring Python virtualenv and dependencies..."
if [ ! -x "venv/bin/python" ]; then
  python3 -m venv venv
fi
./venv/bin/pip install -U pip >/dev/null
./venv/bin/pip install aiohttp matplotlib >/dev/null

# Run incremental benchmark (authoritative)
echo "🏃 Running incremental benchmark (50→1000 users)..."
./venv/bin/python benchmarks/simple_incremental_benchmark.py --max-concurrent 1000 --step 50 --duration 30

# Generate plots
echo "📈 Generating plots..."
./venv/bin/python benchmarks/plot_results.py results/incremental_benchmark_results.json

echo "✅ Benchmark completed!"
echo ""
echo "📊 Outputs:"
echo "- Report:  results/incremental_benchmark_report.md"
echo "- Raw:     results/incremental_benchmark_results.json"
echo "- Plots:   results/throughput_vs_concurrency.png, results/error_rate_vs_concurrency.png"
