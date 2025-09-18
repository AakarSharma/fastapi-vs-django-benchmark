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
docker-compose down -v || true
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 35

# Check if services are running
echo "🔍 Checking service health..."

# Check FastAPI
if curl -s http://localhost:18000/health > /dev/null; then
    echo "✅ FastAPI is running on http://localhost:18000"
else
    echo "❌ FastAPI is not responding"
    exit 1
fi

# Check Django
if curl -s http://localhost:18001/api/benchmark/health/ > /dev/null; then
    echo "✅ Django is running on http://localhost:18001"
else
    echo "❌ Django is not responding"
    exit 1
fi

# Apply Django migrations
echo "🛠️ Applying Django migrations..."
docker-compose exec -T django python manage.py migrate --noinput

# Initialize and upgrade FastAPI (Tortoise) migrations via Aerich
echo "🧭 Running Aerich migrations for FastAPI..."
# If not initialized, init and init-db (creates initial migration and tables); otherwise upgrade
docker-compose exec -T fastapi sh -lc 'if [ -f pyproject.toml ] && [ -d migrations ]; then aerich upgrade; else aerich init -t aerich_cfg.TORTOISE_ORM && aerich init-db; fi'

# Ensure Python venv exists and install dependencies (recreate to avoid bad shebangs)
echo "📋 Ensuring Python virtualenv and dependencies..."
rm -rf venv
python3 -m venv venv
./venv/bin/pip install -U pip >/dev/null
./venv/bin/pip install aiohttp matplotlib >/dev/null

echo "🏃 Running incremental benchmark (10→200 users)..."
./venv/bin/python benchmarks/simple_incremental_benchmark.py --fastapi-url http://localhost:18000 --django-url http://localhost:18001 --max-concurrent 100 --step 10 --duration 10

echo "✅ Smoke benchmark complete. Starting full benchmark..."

# Move outputs to results directory for plotting
mv -f incremental_benchmark_results.json results/incremental_benchmark_results.json || true
mv -f incremental_benchmark_report.md results/incremental_benchmark_report.md || true

# Generate plots
echo "📈 Generating plots..."
./venv/bin/python benchmarks/plot_results.py results/incremental_benchmark_results.json

echo "✅ Benchmark completed!"
echo ""
echo "📊 Outputs:"
echo "- Report:  results/incremental_benchmark_report.md"
echo "- Raw:     results/incremental_benchmark_results.json"
echo "- Plots:   results/throughput_vs_concurrency.png, results/error_rate_vs_concurrency.png"
