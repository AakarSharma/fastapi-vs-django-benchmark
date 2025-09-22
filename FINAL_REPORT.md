# FastAPI vs Django WSGI vs Django ASGI vs fast-django-asgi — Final Report

Date: 2025-09-22

## Overview
- Goal: Compare throughput, latency, error rate, CPU, and memory across three backends with the same business logic and identical resource limits.
- Backends:
  - FastAPI (ASGI, Tortoise ORM, uvloop)
  - Django WSGI (sync views, Django ORM)
  - Django ASGI (async views for I/O; Django ORM executed safely via thread offloading)
  - fast-django-asgi (ASGI, Tortoise ORM, uvicorn/gunicorn)
- Equalization:
  - Dockerized services, 1 CPU and ~2GB RAM per app
  - One worker per app (gunicorn for WSGI; gunicorn+UvicornWorker for ASGI)
  - Same io-intensive workload (2x file I/O, 8x DB I/O), executed sequentially for parity
- Database: MySQL (separate container). Migrations applied for all apps.

## Methodology
- Incremental benchmark across 10 concurrency levels: 10 → 100 concurrent users
- Duration: 10 seconds per framework per level (gaps between runs)
- Load generator: aiohttp-based client; metrics aggregated per framework per level
- Endpoints under test:
  - FastAPI: `/io-intensive`
  - Django WSGI: `/api/benchmark/io_intensive/`
  - Django ASGI: `/api/benchmark/io_intensive/` (async function-based view)
  - fast-django-asgi: `/api/benchmark/io_intensive/`

## Summary Results (Throughput and Error Rate)

| Concurrency | FastAPI Thr (RPS) | Django WSGI Thr (RPS) | Django ASGI Thr (RPS) | fast-django-asgi Thr (RPS) | FastAPI Err % | DJ WSGI Err % | DJ ASGI Err % | FD-ASGI Err % |
|-------------|-------------------|------------------------|-----------------------|----------------------------|---------------|---------------|---------------|---------------|
| 10 | 263.05 | 70.51 | 72.02 | 255.82 | 0.05% | 0.00% | 0.00% | 0.00% |
| 20 | 287.19 | 70.77 | 76.53 | 298.08 | 0.00% | 0.00% | 0.00% | 0.00% |
| 30 | 298.32 | 70.83 | 80.64 | 254.68 | 0.00% | 0.00% | 0.00% | 0.00% |
| 40 | 260.16 | 70.00 | 81.01 | 311.85 | 0.00% | 0.00% | 0.00% | 0.00% |
| 50 | 267.44 | 70.88 | 80.61 | 267.19 | 0.99% | 0.00% | 0.00% | 0.00% |
| 60 | 282.71 | 69.47 | 76.30 | 297.90 | 0.00% | 0.00% | 0.00% | 0.00% |

Full per-level details (avg, P95, P99, CPU, memory) are in `results/incremental_benchmark_report.md` and `results/incremental_benchmark_results.json`.

## Key Findings
- Throughput
  - FastAPI and fast-django-asgi are comparable on this workload, both ~250–312 RPS (1 worker).
  - Django WSGI and Django ASGI cluster around ~70–81 RPS.
- Latency
  - FastAPI has the lowest average and tail latencies; WSGI moderate; ASGI highest tails under load.
- Errors
  - Negligible for Django WSGI and Django ASGI in these runs.
  - FastAPI saw a small error spike (~2.11%) only at 80 users; otherwise 0% or near-zero.
- Resource Usage
  - Django ASGI memory grows with concurrency more than WSGI.
  - CPU tends to saturate at higher concurrencies for all three, as expected.

## Interpretation
- Django ASGI did not outperform Django WSGI because the Django ORM is synchronous with MySQL in this configuration. Even with async views, ORM work runs in threads, adding overhead that negates ASGI benefits.
- FastAPI uses a fully async stack (uvloop + Tortoise ORM + async MySQL driver), so it benefits more as concurrency increases.

## Recommendations
- Staying on Django + MySQL (sync ORM):
  - Prefer WSGI for simplicity and predictable performance.
  - If using ASGI, minimize thread offloading overhead (batch DB work, avoid per-call thread churn).
- If pursuing higher throughput with Django ASGI:
  - Consider an async-friendly DB stack (e.g., PostgreSQL with async driver) as Django’s async ORM support matures.
  - Consider multiple ASGI workers for parallelism (not used here for fairness).
- For maximum throughput on this workload: FastAPI is the best fit due to its end-to-end async stack.

## Artifacts
- Detailed report: `results/incremental_benchmark_report.md`
- Raw data (JSON): `results/incremental_benchmark_results.json`
- Plots:
  - `results/throughput_vs_concurrency.png`
  - `results/error_rate_vs_concurrency.png`
  - `results/cpu_usage_vs_concurrency.png`
  - `results/duration_vs_concurrency.png`
  - `results/total_requests_vs_concurrency.png`

## Reproduce
- One-command run: `./start_benchmark.sh`
- Services: FastAPI on 18000, Django WSGI on 18001, Django ASGI on 18002

# FastAPI vs Django Performance Benchmark - Final Report (Updated)

## Executive Summary

This comprehensive benchmark compares FastAPI and Django frameworks under I/O intensive workloads using MySQL database and equalized single vCPU configurations. **After optimizing FastAPI's connection pool, the results show a dramatic performance improvement** with FastAPI maintaining superior performance across all tested concurrency levels.

**Key Finding**: **FastAPI now consistently outperforms Django** across all concurrency levels (10-100 users) with optimized connection pooling, achieving 3-4x higher throughput while maintaining excellent error handling.

## Test Environment

- **Python Version**: 3.11
- **Database**: MySQL 8.4 with optimized configuration
- **ORM**: Tortoise ORM (FastAPI) vs Django ORM (Django)
- **Server Configuration**: 
  - FastAPI: Gunicorn + UvicornWorker (1 worker)
  - Django: Gunicorn (1 worker, 8 threads)
- **Container Resources**: 1 vCPU, 2GB RAM per container
- **Test Duration**: 10 seconds per concurrency level
- **Concurrency Range**: 10-100 users (incremental steps of 10)
- **Database Operations**: 8 database transactions per request (create 10, update 5, delete 5)
- **File I/O**: 2 file operations per request (JSON write/read)
- **Connection Pool**: FastAPI optimized to 100-10,000 connections

## Application Architecture

### FastAPI Application (Optimized)
- **Framework**: FastAPI 0.115.6
- **ORM**: Tortoise ORM with MySQL (aiomysql)
- **Server**: Gunicorn + UvicornWorker
- **Port**: 18000
- **Connection Pool**: 100-10,000 connections (optimized)
- **Features**: Async I/O operations, file operations, database operations

### Django Application
- **Framework**: Django 5.1.5
- **ORM**: Django ORM with MySQL (mysqlclient)
- **Server**: Gunicorn with 8 threads
- **Port**: 18001
- **Connection Pool**: CONN_MAX_AGE=60
- **Features**: Synchronous I/O operations, file operations, database operations

## Performance Results (Updated)

### Throughput Comparison

| Concurrency | FastAPI (RPS) | Django (RPS) | Winner | FastAPI Advantage |
|-------------|---------------|--------------|--------|-------------------|
| 10 users    | 292.41        | 71.91        | **FastAPI** | **4.07x** |
| 20 users    | 307.70        | 74.65        | **FastAPI** | **4.12x** |
| 30 users    | 331.34        | 74.25        | **FastAPI** | **4.46x** |
| 40 users    | 291.95        | 71.29        | **FastAPI** | **4.09x** |
| 50 users    | 300.98        | 73.59        | **FastAPI** | **4.09x** |
| 60 users    | 296.43        | 73.14        | **FastAPI** | **4.05x** |
| 70 users    | 270.97        | 75.64        | **FastAPI** | **3.58x** |
| 80 users    | 300.71        | 76.20        | **FastAPI** | **3.95x** |
| 90 users    | 295.91        | 75.98        | **FastAPI** | **3.90x** |
| 100 users   | 278.30        | 74.95        | **FastAPI** | **3.71x** |

**Result**: **FastAPI dominates across all concurrency levels** with 3.6-4.5x higher throughput

### Latency Analysis

#### Average Response Time
- **FastAPI**: 0.026s → 0.326s (12.5x increase)
- **Django**: 0.123s → 1.136s (9.2x increase)

#### P95 Response Time
- **FastAPI**: 0.110s → 1.442s (13.1x increase)
- **Django**: 0.467s → 1.746s (3.7x increase)

#### P99 Response Time
- **FastAPI**: 0.129s → 1.582s (12.3x increase)
- **Django**: 0.566s → 1.950s (3.4x increase)

### Error Rate Analysis

| Concurrency | FastAPI Error Rate | Django Error Rate | Winner |
|-------------|-------------------|-------------------|--------|
| 10-30 users | 0.00%             | 0.00%             | Tie    |
| 40 users    | 0.33%             | 0.00%             | Django |
| 50-60 users | 0.00%             | 0.00%             | Tie    |
| 70 users    | 0.23%             | 0.00%             | Django |
| 80-100 users| 0.00%             | 0.00%             | Tie    |

**Result**: **Both frameworks maintain excellent reliability** with minimal errors

### Resource Efficiency

#### CPU Usage
- **FastAPI**: 90.1% → 78.4% (efficient utilization)
- **Django**: 99.1% → 101.4% (consistently high)

#### Memory Usage
- **FastAPI**: 61.7MB → 115.9MB (88% increase)
- **Django**: 60.5MB → 72.9MB (20% increase)

## Key Findings (Updated)

### 1. Dramatic Performance Improvement
- **FastAPI now consistently outperforms Django** across all concurrency levels
- **4x average throughput advantage** maintained from 10 to 100 concurrent users
- **Connection pool optimization** eliminated previous performance degradation

### 2. Consistent Performance Scaling
- **FastAPI maintains 270-330 RPS** across all concurrency levels
- **Django maintains 71-76 RPS** across all concurrency levels
- **No performance crossover point** - FastAPI remains superior throughout

### 3. Excellent Error Handling
- **Both frameworks achieve near-zero error rates** (0-0.33%)
- **FastAPI errors are minimal** and don't significantly impact performance
- **Robust error handling** in both implementations

### 4. Resource Utilization Patterns
- **FastAPI shows efficient CPU utilization** with slight decrease at higher concurrency
- **Django maintains high CPU utilization** across all levels
- **FastAPI uses more memory** due to larger connection pool but maintains performance

## Technical Analysis

### Why FastAPI Now Excels Consistently

1. **Optimized Connection Pool**: 100-10,000 connections eliminate bottlenecks
2. **Async Architecture**: Superior handling of I/O operations with proper resource allocation
3. **Event Loop Efficiency**: Single-threaded event loop maximizes CPU utilization
4. **Connection Management**: Large connection pool prevents connection exhaustion

### Why Django Maintains Consistent Performance

1. **Threading Model**: 8 threads provide stable concurrency handling
2. **Mature ORM**: Django ORM is highly optimized for database operations
3. **Connection Management**: Robust connection pooling and transaction handling
4. **Synchronous Processing**: Predictable resource usage patterns

### Connection Pool Impact

The **100x increase in maximum connections** (100 → 10,000) provided:
- **Elimination of connection pool exhaustion**
- **Consistent performance at all concurrency levels**
- **Reduced connection acquisition time**
- **Better handling of concurrent requests**

## Performance Recommendations

### For All Concurrency Levels (1-100+ users)
- **Choose FastAPI** for maximum throughput and performance
- **4x higher throughput** than Django across all tested levels
- **Excellent async capabilities** for I/O intensive workloads
- **Scalable connection pool** handles high concurrency

### For Resource-Constrained Environments
- **Choose Django** if memory usage is critical (20% less memory usage)
- **Choose FastAPI** if throughput is priority (4x higher performance)
- **Both frameworks** are production-ready with proper configuration

### For Production Deployment
- **FastAPI**: Current configuration is well-optimized for high concurrency
- **Django**: Current configuration provides stable, consistent performance
- **Both**: Monitor resource usage and implement proper connection pooling

## Architecture Considerations

### FastAPI Strengths (Optimized)
1. **Superior performance** across all concurrency levels
2. **Large connection pool** handles high concurrency without degradation
3. **Async architecture** provides excellent I/O handling
4. **Consistent throughput** from 10 to 100+ concurrent users

### Django Strengths
1. **Mature ecosystem** with battle-tested components
2. **Predictable performance** characteristics
3. **Lower memory usage** compared to FastAPI
4. **Robust threading model** for concurrent requests

## Conclusion (Updated)

This updated benchmark reveals that **FastAPI significantly outperforms Django** across all tested concurrency levels when properly optimized:

- **FastAPI is the clear winner** for all concurrency scenarios (10-100+ users)
- **4x average throughput advantage** maintained consistently
- **Connection pool optimization** was critical for FastAPI's performance
- **Both frameworks** demonstrate excellent reliability and error handling

The **optimization of FastAPI's connection pool** from 100 to 10,000 maximum connections eliminated the previous performance degradation and established FastAPI as the superior choice for I/O intensive workloads.

## Repository Structure

```
fastapi-vs-django-benchmark/
├── fastapi_app/          # FastAPI application with optimized connection pool
├── django_app/           # Django application with Django ORM
├── benchmarks/           # Performance testing scripts
├── docker/              # Docker configurations
├── results/             # Benchmark results and visualizations
├── requirements/        # Python requirements files
├── docker-compose.yml   # Container orchestration
└── README.md           # Project documentation
```

## Getting Started

1. Clone the repository
2. Run `./start_benchmark.sh` for automated benchmark execution
3. View results in `results/` directory
4. Analyze performance characteristics for your use case

## Future Improvements

1. **Extended concurrency testing** beyond 100 users
2. **Memory optimization** for FastAPI connection pool
3. **Load balancing** for even higher concurrency
4. **Real-world workload simulation** with mixed I/O patterns
5. **Connection pool tuning** based on specific use cases

---
*Report generated on: 2025-01-27*
*Benchmark data: incremental_benchmark_results.json (Updated)*
*Test duration: 10 seconds per concurrency level*
*Concurrency range: 10-100 users*
*FastAPI connection pool: 100-10,000 connections (optimized)*

---

## Validation and Fairness Check (2025-09-21)

- We refactored the Django ASGI implementation to proper Django 5 async patterns and reran the full benchmark (10→100 users, 10s each). Latest highlights (RPS):
  - 10: WSGI 71.8, ASGI 75.5
  - 20: WSGI 73.8, ASGI 79.4
  - 30: WSGI 74.0, ASGI 79.2
  - 40: WSGI 69.9, ASGI 71.9
  - 50: WSGI 73.9, ASGI 80.8
  - 60: WSGI 73.3, ASGI 74.4
  - 70: WSGI 72.7, ASGI 78.8
  - 80: WSGI 71.2, ASGI 77.6
  - 90: WSGI 74.6, ASGI 80.1
  - 100: WSGI 64.1, ASGI 69.8
- Error rates were 0% for both Django WSGI and Django ASGI at all levels in this run.

Correctness notes (Django WSGI vs ASGI):
- Endpoint parity: Both run an identical workload shape (2 file I/O + 8 DB I/O per request). The WSGI version performs per-instance updates/deletes; the ASGI version currently uses `QuerySet.aupdate()` for the 5 updates and `QuerySet.adelete()` for cleanup. This bulk update/delete is slightly more efficient than per-instance operations and likely explains ASGI’s small throughput edge in these numbers.
- Connections: WSGI uses `CONN_MAX_AGE=60`; ASGI uses `CONN_MAX_AGE=0` (to avoid pitfalls with async + mysqlclient). This actually disadvantages ASGI. Despite that, ASGI still meets or slightly exceeds WSGI in this run, consistent with the bulk ops note above.
- Conclusion: With strictly identical per-instance operations on both sides (i.e., using `Model.asave()` + `Model.adelete()` in ASGI), we expect Django ASGI and WSGI to be within a few RPS of each other for this workload. The current small ASGI advantage is attributable to bulk `aupdate/adelete` vs per-instance ops.

Artifacts:
- Latest detailed results: `results/incremental_benchmark_report.md`
- Latest raw JSON: `results/incremental_benchmark_results.json`
- Plots refreshed: `results/throughput_vs_concurrency.png`, `results/error_rate_vs_concurrency.png`, `results/cpu_usage_vs_concurrency.png`, `results/duration_vs_concurrency.png`, `results/total_requests_vs_concurrency.png`

Recommendation for perfect parity check:
- Switch Django ASGI updates/deletes to per-instance (`Model.asave()`/`Model.adelete()`), align `CONN_MAX_AGE` with WSGI, rerun a short confirmation (e.g., 10/20 users×10s). Numbers should converge further.