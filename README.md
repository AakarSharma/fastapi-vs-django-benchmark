# FastAPI vs Django Performance Benchmark (Reproducible)

This repository compares FastAPI and Django under identical, I/O‑intensive workloads with equalized resources. It is designed for one‑command setup, reproducible runs, and a single consolidated report with plots.

## What This Contains
- Two apps exposing identical endpoints and doing the same work:
  - FastAPI (+ Tortoise ORM, asyncpg)
  - Django (+ Django ORM, psycopg2)
- PostgreSQL in Docker shared by both
- Identical I/O workload per request:
  - 5× file I/O (JSON write/read to per‑request unique temp file)
  - 3× database I/O (create 10, update 5, delete 5) in a single DB transaction
  - Unique emails under high concurrency to avoid collisions
- Equalized resources: 1 vCPU, 2 GB RAM per service
- Incremental benchmark script and plot generation

## Prerequisites
- macOS/Linux (or WSL2)
- Docker and Docker Compose
- Python 3.11+ on host (for running the benchmark)

## Equal Resources and Server Settings
Configured in `docker-compose.yml` and Dockerfiles:
- CPU: 1 vCPU per service (`cpus: 1.0`)
- Memory: 2 GB per service (`mem_limit: 2g`)
- Database: PostgreSQL 15 (tuned via Compose)
- FastAPI server: Uvicorn with `--workers 1`, `--loop uvloop`, `--http httptools`
- Django server: Gunicorn with `-w 1 --threads 4`

## Project Structure
```
fastapi-vs-django-benchmark/
├── fastapi_app/
├── django_app/
├── benchmarks/
│   ├── simple_incremental_benchmark.py   # Incremental benchmark (50→1000)
│   └── plot_results.py                   # Generate PNG plots
├── docker/
├── docker-compose.yml
├── results/
└── start_benchmark.sh                    # One‑command run
```

## 1) One‑Command Reproducible Run
```bash
./start_benchmark.sh
```
This builds the images, starts containers, runs migrations, executes the incremental benchmark (50→1000 users), and generates plots.

Outputs:
- `results/incremental_benchmark_results.json`
- `results/incremental_benchmark_report.md`
- `results/throughput_vs_concurrency.png`
- `results/error_rate_vs_concurrency.png`

## 2) Manual Run (Optional)
Start services:
```bash
docker-compose up --build -d
```
Migrate Django:
```bash
docker compose exec django python manage.py migrate
```
Create venv and install deps:
```bash
python -m venv venv
source venv/bin/activate
pip install aiohttp matplotlib
```
Run the benchmark:
```bash
python benchmarks/simple_incremental_benchmark.py --max-concurrent 1000 --step 50 --duration 30
python benchmarks/plot_results.py results/incremental_benchmark_results.json
```

## Methodology (Fairness & Parity)
- Same endpoints and same work in both apps (CRUD + file I/O) per request to `/io-intensive`.
- Per‑request unique temp file to avoid collisions.
- DB operations wrapped in a single transaction for both frameworks.
- Unique emails using timestamp+UUID under high concurrency.
- Identical hardware constraints (1 vCPU, 2 GB) enforced via Docker Compose.

## Troubleshooting
- Django `/io-intensive` path is `/api/benchmark/io_intensive/` (underscore).
- If DB connection errors appear, consider raising Postgres `max_connections` in Compose or reducing threads.
- Tail latencies near ~60s indicate saturation and client timeouts; reduce per‑request work or scale resources.

## License
MIT
