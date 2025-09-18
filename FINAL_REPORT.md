# FastAPI vs Django Performance Benchmark - Final Report

## Executive Summary

This comprehensive benchmark compares FastAPI and Django frameworks under I/O intensive workloads using MySQL database and equalized single vCPU configurations. The test reveals a **clear performance crossover point** where FastAPI excels at low concurrency but Django maintains consistent performance at higher concurrency levels.

**Key Finding**: FastAPI shows superior performance at low concurrency (10-30 users) but Django demonstrates better sustained performance at medium to high concurrency (40+ users).

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

## Application Architecture

### FastAPI Application
- **Framework**: FastAPI 0.115.6
- **ORM**: Tortoise ORM with MySQL (aiomysql)
- **Server**: Gunicorn + UvicornWorker
- **Port**: 18000
- **Features**: Async I/O operations, file operations, database operations
- **Connection Pool**: 20-100 connections

### Django Application
- **Framework**: Django 5.1.5
- **ORM**: Django ORM with MySQL (mysqlclient)
- **Server**: Gunicorn with 8 threads
- **Port**: 18001
- **Features**: Synchronous I/O operations, file operations, database operations
- **Connection Pool**: CONN_MAX_AGE=60

## I/O Intensive Operations

Both applications implement identical I/O intensive workloads per request:
- **File I/O**: 2× JSON file write/read operations with unique temp files
- **Database I/O**: 8× database transactions (create 10 users, update 5, delete 5)
- **Transaction Safety**: All database operations wrapped in atomic transactions
- **Concurrency Safety**: Unique identifiers prevent data collisions

## Performance Results

### Throughput Comparison

| Concurrency | FastAPI (RPS) | Django (RPS) | Winner | FastAPI Advantage |
|-------------|---------------|--------------|--------|-------------------|
| 10 users    | 288.02        | 76.16        | FastAPI | 3.78x |
| 20 users    | 174.20        | 71.79        | FastAPI | 2.43x |
| 30 users    | 125.06        | 70.09        | FastAPI | 1.78x |
| 40 users    | 72.43         | 75.20        | Django  | -0.04x |
| 50 users    | 57.11         | 76.23        | Django  | -0.25x |
| 60 users    | 41.23         | 74.45        | Django  | -0.45x |
| 70 users    | 43.58         | 70.08        | Django  | -0.38x |
| 80 users    | 34.83         | 74.53        | Django  | -0.53x |
| 90 users    | 32.33         | 76.25        | Django  | -0.58x |
| 100 users   | 27.44         | 76.77        | Django  | -0.64x |

**Crossover Point**: 40 concurrent users

### Latency Analysis

#### Average Response Time
- **FastAPI**: 0.027s → 3.272s (121x increase)
- **Django**: 0.116s → 1.115s (9.6x increase)

#### P95 Response Time
- **FastAPI**: 0.123s → 17.087s (139x increase)
- **Django**: 0.461s → 1.846s (4x increase)

#### P99 Response Time
- **FastAPI**: 0.154s → 17.309s (112x increase)
- **Django**: 0.516s → 2.160s (4.2x increase)

### Resource Efficiency

#### CPU Usage
- **FastAPI**: 84.9% → 21.3% (decreasing with concurrency)
- **Django**: 97.8% → 101.6% (consistently high)

#### Memory Usage
- **FastAPI**: 60.7MB → 81.1MB (33% increase)
- **Django**: 60.3MB → 72.0MB (19% increase)

## Key Findings

### 1. Performance Crossover Point
- **FastAPI excels at low concurrency** (10-30 users) with 1.78-3.78x higher throughput
- **Django maintains consistent performance** across all concurrency levels
- **Crossover occurs at 40 concurrent users** where Django begins to outperform FastAPI

### 2. Latency Characteristics
- **FastAPI shows dramatic latency degradation** at higher concurrency (121x increase)
- **Django maintains stable latency** with only 9.6x increase from low to high concurrency
- **Django's P95/P99 latencies are significantly more predictable**

### 3. Resource Utilization Patterns
- **FastAPI CPU usage decreases** with higher concurrency (potential underutilization)
- **Django maintains high CPU utilization** across all concurrency levels
- **Both frameworks show similar memory efficiency**

### 4. Error Handling
- **Both frameworks achieved 0% error rate** across all concurrency levels
- **No connection drops or timeouts** observed in the test range
- **Robust error handling** in both implementations

## Technical Analysis

### Why FastAPI Excels at Low Concurrency

1. **Async Architecture**: Superior handling of I/O operations with minimal overhead
2. **Event Loop Efficiency**: Single-threaded event loop maximizes CPU utilization for I/O-bound tasks
3. **Connection Pooling**: Efficient async connection management
4. **Lower Framework Overhead**: Minimal request processing overhead

### Why Django Maintains Performance at High Concurrency

1. **Threading Model**: 8 threads provide better concurrency handling under load
2. **Mature ORM**: Django ORM is highly optimized for database operations
3. **Connection Management**: Robust connection pooling and transaction handling
4. **Synchronous Processing**: Predictable resource usage patterns

### Why FastAPI Degrades at High Concurrency

1. **Event Loop Saturation**: Single event loop becomes bottleneck
2. **Connection Pool Exhaustion**: Limited async connection pool (20-100)
3. **Memory Pressure**: Increasing memory usage affects performance
4. **Context Switching Overhead**: Async context switching becomes expensive

## Performance Recommendations

### For Low-Medium Concurrency (1-40 users)
- **Choose FastAPI** for maximum throughput and lowest latency
- Ideal for microservices, APIs, and low-traffic applications
- Excellent resource efficiency and async capabilities

### For High Concurrency (40+ users)
- **Choose Django** for consistent, predictable performance
- Better suited for high-traffic web applications
- More stable latency characteristics under load

### For Production Deployment
- **FastAPI**: Consider multiple workers or async connection pool tuning
- **Django**: Current configuration is well-optimized for the tested workload
- **Both**: Monitor resource usage and implement proper connection pooling

## Architecture Considerations

### FastAPI Optimization Opportunities
1. **Increase worker count** for higher concurrency
2. **Tune connection pool size** based on expected load
3. **Implement connection pooling strategies** for database operations
4. **Consider async task queues** for heavy I/O operations

### Django Strengths
1. **Mature ecosystem** with battle-tested components
2. **Predictable performance** characteristics
3. **Excellent ORM** with built-in optimizations
4. **Robust threading model** for concurrent requests

## Conclusion

This benchmark reveals that **both frameworks excel in different scenarios**:

- **FastAPI is the clear winner for low to medium concurrency** applications where async I/O provides significant advantages
- **Django provides more consistent and predictable performance** at higher concurrency levels
- **The choice depends on your expected concurrency patterns** and performance requirements

The **crossover point at 40 concurrent users** provides a clear decision framework:
- **< 40 concurrent users**: FastAPI recommended
- **≥ 40 concurrent users**: Django recommended

Both frameworks are production-ready and demonstrate excellent error handling and resource efficiency within their optimal ranges.

## Repository Structure

```
fastapi-vs-django-benchmark/
├── fastapi_app/          # FastAPI application with Tortoise ORM
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

1. **Multi-worker FastAPI testing** to compare with Django's threading model
2. **Connection pool optimization** for both frameworks
3. **Memory profiling** to understand resource usage patterns
4. **Extended concurrency testing** beyond 100 users
5. **Real-world workload simulation** with mixed I/O patterns

---
*Report generated on: 2025-01-27*
*Benchmark data: incremental_benchmark_results.json*
*Test duration: 10 seconds per concurrency level*
*Concurrency range: 10-100 users*