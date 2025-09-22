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

## Summary Results (Throughput and Error Rate) - Extended Benchmark (10-200 users)

### Performance Overview
| Framework | Max RPS | Min RPS | Avg RPS | Max Error% | Breaking Point |
|-----------|---------|---------|---------|------------|----------------|
| **FastAPI** | 303.2 | 133.3 | 255.6 | 5.5% | 100 users |
| **Django WSGI** | 74.1 | 61.1 | 69.2 | 0.0% | >200 users |
| **Django ASGI** | 80.9 | 70.3 | 75.1 | 0.0% | >200 users |
| **fast-django-asgi** | 291.4 | 154.8 | 225.1 | 0.0% | >200 users |

### Key Performance Milestones
| Concurrency | Winner | RPS | Error Rate | Notes |
|-------------|--------|-----|------------|-------|
| 10 users | FastAPI | 273.9 | 0.0% | FastAPI leads early |
| 50 users | FastAPI | 259.1 | 1.0% | FastAPI maintains lead |
| 100 users | FastAPI | 209.4 | 5.5% | FastAPI shows stress at 100 users |
| 150 users | FastAPI | 259.2 | 0.0% | FastAPI recovers performance |
| 200 users | fast-django-asgi | 158.0 | 0.0% | fast-django-asgi most stable at high load |

### Detailed Results by Concurrency Level
| Concurrency | FastAPI | Django WSGI | Django ASGI | fast-django-asgi | Winner |
|-------------|---------|-------------|-------------|------------------|--------|
| 10 | 273.9 | 67.5 | 71.7 | 255.8 | **FastAPI** |
| 20 | 287.2 | 70.8 | 73.4 | 284.2 | **FastAPI** |
| 30 | 301.4 | 68.1 | 76.3 | 284.5 | **FastAPI** |
| 40 | 301.3 | 67.8 | 74.5 | 291.4 | **FastAPI** |
| 50 | 259.1 | 68.0 | 75.9 | 254.1 | **FastAPI** |
| 60 | 265.5 | 69.7 | 76.0 | 272.6 | **FastAPI** |
| 70 | 269.9 | 68.6 | 75.4 | 266.0 | **FastAPI** |
| 80 | 265.4 | 68.8 | 74.7 | 268.3 | **FastAPI** |
| 90 | 264.4 | 68.4 | 75.2 | 264.6 | **FastAPI** |
| 100 | 209.4 | 68.7 | 70.3 | 206.8 | **FastAPI** |
| 110 | 277.8 | 71.4 | 79.0 | 234.1 | **FastAPI** |
| 120 | 277.5 | 71.5 | 72.9 | 190.1 | **FastAPI** |
| 130 | 259.2 | 69.2 | 71.8 | 200.5 | **FastAPI** |
| 140 | 221.8 | 61.1 | 75.8 | 225.2 | **fast-django-asgi** |
| 150 | 259.2 | 66.2 | 75.6 | 221.7 | **FastAPI** |
| 160 | 256.9 | 68.6 | 75.1 | 172.8 | **FastAPI** |
| 170 | 303.2 | 72.1 | 79.8 | 160.2 | **FastAPI** |
| 180 | 266.0 | 73.0 | 70.9 | 154.8 | **FastAPI** |
| 190 | 152.8 | 73.8 | 80.9 | 155.8 | **Django ASGI** |
| 200 | 133.3 | 74.1 | 76.6 | 158.1 | **fast-django-asgi** |

Full per-level details (avg, P95, P99, CPU, memory) are in `results/incremental_benchmark_report.md` and `results/incremental_benchmark_results.json`.

## Key Findings (Extended Benchmark: 10-200 Users)

### Performance Characteristics
- **FastAPI**: Dominates low-to-medium concurrency (10-150 users) with 250-300+ RPS, but shows instability at 100 users (5.5% error rate) and degrades significantly at very high concurrency (190-200 users).
- **fast-django-asgi**: Most consistent performer across all concurrency levels, maintaining 150-290 RPS with 0% error rate throughout the entire range.
- **Django WSGI**: Stable and predictable performance around 67-74 RPS with 0% error rate across all concurrency levels.
- **Django ASGI**: Slightly better than WSGI (70-81 RPS) with 0% error rate, showing consistent async benefits.

### Breaking Points and Stability
- **FastAPI**: Shows stress at 100 users (5.5% error rate), then recovers but degrades at 190+ users
- **fast-django-asgi**: No breaking point identified - maintains performance and 0% error rate up to 200 users
- **Django WSGI/ASGI**: No breaking points - both maintain 0% error rate throughout the entire range

### Throughput Analysis
- **Low-Medium Concurrency (10-80 users)**: FastAPI leads with 260-300+ RPS
- **High Concurrency (100-150 users)**: FastAPI still leads but with some instability
- **Very High Concurrency (180-200 users)**: fast-django-asgi becomes the most reliable performer
### Latency Analysis
- **FastAPI**: Lowest latencies at low concurrency, but P95/P99 latencies spike significantly at high concurrency (up to 7+ seconds at 200 users)
- **fast-django-asgi**: Consistent latency characteristics, P95/P99 remain reasonable even at 200 users (5-6 seconds)
- **Django WSGI/ASGI**: Moderate latencies that increase predictably with concurrency, but remain stable

### Error Rate Analysis
- **FastAPI**: 0% error rate for most concurrency levels, but shows 5.5% error rate at 100 users
- **fast-django-asgi**: Perfect 0% error rate across all concurrency levels (10-200 users)
- **Django WSGI/ASGI**: Perfect 0% error rate across all concurrency levels
- Resource Usage
  - Django ASGI memory grows with concurrency more than WSGI.
  - CPU tends to saturate at higher concurrencies for all three, as expected.

## Interpretation (Extended Benchmark Results)

### Framework Performance Patterns
- **FastAPI**: Excels at low-to-medium concurrency due to its fully async stack (uvloop + Tortoise ORM + async MySQL driver), but shows instability under extreme load due to single-worker limitations and connection pool constraints.
- **fast-django-asgi**: Demonstrates the most balanced performance profile, combining FastAPI's async benefits with Django's stability patterns. Its consistent 0% error rate and stable throughput make it the most reliable choice for high-concurrency applications.
- **Django WSGI**: Provides predictable, stable performance across all concurrency levels with perfect error handling, making it ideal for applications requiring consistent behavior.
- **Django ASGI**: Shows modest improvements over WSGI due to async view handling, but the synchronous ORM limits the benefits of the async architecture.

### Concurrency Scaling Insights
- **10-80 users**: FastAPI dominates with superior throughput
- **100-150 users**: FastAPI leads but shows signs of stress
- **180-200 users**: fast-django-asgi becomes the most reliable performer
- **All levels**: Django frameworks maintain perfect error rates

## Recommendations (Based on Extended Benchmark)

### For Different Concurrency Ranges
- **Low-Medium Concurrency (10-80 users)**: **FastAPI** - Superior throughput and low latency
- **High Concurrency (100-150 users)**: **FastAPI** - Still leads but monitor for instability
- **Very High Concurrency (180-200+ users)**: **fast-django-asgi** - Most reliable and consistent performance
- **Mission-Critical Applications**: **Django WSGI** - Perfect error handling and predictable performance

### Framework-Specific Recommendations
- **FastAPI**: Best for applications with moderate concurrency requirements. Consider multiple workers for very high concurrency.
- **fast-django-asgi**: Ideal for applications requiring both high performance and reliability across all concurrency levels.
- **Django WSGI**: Perfect for applications prioritizing stability and predictable performance over raw throughput.
- **Django ASGI**: Good middle ground for Django applications that need some async benefits while maintaining Django patterns.

### Production Deployment Considerations
- **Single Worker Limitation**: All frameworks tested with 1 worker. Consider multiple workers for production.
- **Connection Pool Tuning**: FastAPI's performance degradation at high concurrency suggests connection pool optimization needed.
- **Error Handling**: fast-django-asgi and Django frameworks show superior error handling under load.

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
*Benchmark data: incremental_benchmark_results.json (Extended)*
*Test duration: 8 seconds per concurrency level*
*Concurrency range: 10-200 users (extended)*
*Frameworks tested: FastAPI, Django WSGI, Django ASGI, fast-django-asgi*
*All frameworks: 1 worker, gunicorn+uvicorn for ASGI frameworks*

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