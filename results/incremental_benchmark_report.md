# Incremental Benchmark Report: FastAPI vs Django WSGI vs Django ASGI

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 60 users
- **Step Size**: 50 users
- **Total Tests**: 8 concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ WSGI Thr (RPS) | DJ ASGI Thr (RPS) | FAPI Err % | DJ WSGI Err % | DJ ASGI Err % | Winner |
|-------------|----------------|-------------------|-------------------|------------|---------------|---------------|--------|
| 10 | 263.05 | 70.51 | 72.02 | 0.05% | 0.00% | 0.00% | FastAPI |
| 10 | 255.82 | 287.19 | 70.77 | 0.00% | 0.00% | 0.00% | Django WSGI |
| 20 | 76.53 | 298.08 | 298.32 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 30 | 70.83 | 80.64 | 254.68 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 40 | 260.16 | 70.00 | 81.01 | 0.00% | 0.00% | 0.00% | FastAPI |
| 40 | 311.85 | 267.44 | 70.88 | 0.00% | 0.99% | 0.00% | FastAPI |
| 50 | 80.61 | 267.19 | 282.71 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 60 | 69.47 | 76.30 | 297.90 | 0.00% | 0.00% | 0.00% | Django ASGI |

## Detailed Results

### FastAPI Results

#### 10 Concurrent Users
- **Throughput**: 263.05 RPS
- **Error Rate**: 0.05%
- **Avg Response Time**: 0.030s
- **P95 Response Time**: 0.126s
- **P99 Response Time**: 0.138s
- **Avg CPU**: 71.9%
- **Avg Memory**: 64.2MB (max 64.9MB)

#### 20 Concurrent Users
- **Throughput**: 287.19 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.060s
- **P95 Response Time**: 0.251s
- **P99 Response Time**: 0.264s
- **Avg CPU**: 75.3%
- **Avg Memory**: 66.1MB (max 66.3MB)

#### 30 Concurrent Users
- **Throughput**: 298.32 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.089s
- **P95 Response Time**: 0.374s
- **P99 Response Time**: 0.392s
- **Avg CPU**: 76.5%
- **Avg Memory**: 73.5MB (max 75.9MB)

#### 40 Concurrent Users
- **Throughput**: 260.16 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.137s
- **P95 Response Time**: 0.576s
- **P99 Response Time**: 0.736s
- **Avg CPU**: 81.5%
- **Avg Memory**: 76.4MB (max 76.5MB)

#### 50 Concurrent Users
- **Throughput**: 267.44 RPS
- **Error Rate**: 0.99%
- **Avg Response Time**: 0.166s
- **P95 Response Time**: 0.629s
- **P99 Response Time**: 1.068s
- **Avg CPU**: 77.0%
- **Avg Memory**: 97.2MB (max 112.5MB)

#### 60 Concurrent Users
- **Throughput**: 282.71 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.192s
- **P95 Response Time**: 0.813s
- **P99 Response Time**: 0.856s
- **Avg CPU**: 81.7%
- **Avg Memory**: 99.8MB (max 100.1MB)

### Django WSGI Results

#### 10 Concurrent Users
- **Throughput**: 70.51 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.127s
- **P95 Response Time**: 0.471s
- **P99 Response Time**: 0.638s
- **Avg CPU**: 81.4%
- **Avg Memory**: 60.7MB (max 65.9MB)

#### 20 Concurrent Users
- **Throughput**: 70.77 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.257s
- **P95 Response Time**: 0.681s
- **P99 Response Time**: 0.771s
- **Avg CPU**: 86.2%
- **Avg Memory**: 65.6MB (max 66.2MB)

#### 30 Concurrent Users
- **Throughput**: 70.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.381s
- **P95 Response Time**: 0.846s
- **P99 Response Time**: 0.928s
- **Avg CPU**: 95.0%
- **Avg Memory**: 65.8MB (max 66.3MB)

#### 40 Concurrent Users
- **Throughput**: 70.00 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.505s
- **P95 Response Time**: 0.953s
- **P99 Response Time**: 1.223s
- **Avg CPU**: 101.9%
- **Avg Memory**: 66.5MB (max 66.7MB)

#### 50 Concurrent Users
- **Throughput**: 70.88 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.616s
- **P95 Response Time**: 1.187s
- **P99 Response Time**: 1.314s
- **Avg CPU**: 101.9%
- **Avg Memory**: 66.9MB (max 67.2MB)

#### 60 Concurrent Users
- **Throughput**: 69.47 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.768s
- **P95 Response Time**: 1.296s
- **P99 Response Time**: 1.405s
- **Avg CPU**: 81.5%
- **Avg Memory**: 66.5MB (max 67.4MB)

### Django ASGI Results

#### 10 Concurrent Users
- **Throughput**: 72.02 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.123s
- **P95 Response Time**: 0.451s
- **P99 Response Time**: 0.560s
- **Avg CPU**: 99.3%
- **Avg Memory**: 51.0MB (max 52.2MB)

#### 20 Concurrent Users
- **Throughput**: 76.53 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.236s
- **P95 Response Time**: 0.858s
- **P99 Response Time**: 0.952s
- **Avg CPU**: 81.6%
- **Avg Memory**: 56.5MB (max 57.0MB)

#### 30 Concurrent Users
- **Throughput**: 80.64 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.334s
- **P95 Response Time**: 1.190s
- **P99 Response Time**: 1.241s
- **Avg CPU**: 96.2%
- **Avg Memory**: 67.2MB (max 71.7MB)

#### 40 Concurrent Users
- **Throughput**: 81.01 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.443s
- **P95 Response Time**: 1.588s
- **P99 Response Time**: 1.634s
- **Avg CPU**: 84.0%
- **Avg Memory**: 73.3MB (max 74.5MB)

#### 50 Concurrent Users
- **Throughput**: 80.61 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.548s
- **P95 Response Time**: 1.965s
- **P99 Response Time**: 2.025s
- **Avg CPU**: 97.1%
- **Avg Memory**: 75.9MB (max 77.0MB)

#### 60 Concurrent Users
- **Throughput**: 76.30 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.709s
- **P95 Response Time**: 2.500s
- **P99 Response Time**: 2.611s
- **Avg CPU**: 103.6%
- **Avg Memory**: 78.9MB (max 79.2MB)

## Analysis

### Performance Trends
- **FastAPI**: Shows async advantages at higher concurrency
- **Django WSGI**: Maintains consistent performance
- **Django ASGI**: Shows async advantages similar to FastAPI

### Breaking Points
- **FastAPI Breaking Point**: 60 users
- **Django WSGI Breaking Point**: 60 users
- **Django ASGI Breaking Point**: 60 users

### Recommendations
- **For Low-Medium Concurrency**: All frameworks perform well
- **For High Concurrency**: FastAPI shows better async performance
- **For Reliability**: Django WSGI shows better error handling
- **For Django Migration**: Django ASGI provides a good middle ground between Django WSGI and FastAPI

---
*Report generated on: 2025-09-22 11:54:39*
