# Incremental Benchmark Report: FastAPI vs Django

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 100 users
- **Step Size**: 50 users
- **Total Tests**: 10 concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ Thr (RPS) | FAPI Err % | DJ Err % | Winner |
|-------------|----------------|--------------|------------|----------|--------|
| 10 | 292.41 | 71.91 | 0.00% | 0.00% | FastAPI |
| 20 | 307.70 | 74.65 | 0.00% | 0.00% | FastAPI |
| 30 | 331.34 | 74.25 | 0.00% | 0.00% | FastAPI |
| 40 | 291.95 | 71.29 | 0.33% | 0.00% | FastAPI |
| 50 | 300.98 | 73.59 | 0.00% | 0.00% | FastAPI |
| 60 | 296.43 | 73.14 | 0.00% | 0.00% | FastAPI |
| 70 | 270.97 | 75.64 | 0.23% | 0.00% | FastAPI |
| 80 | 300.71 | 76.20 | 0.00% | 0.00% | FastAPI |
| 90 | 295.91 | 75.98 | 0.00% | 0.00% | FastAPI |
| 100 | 278.30 | 74.95 | 0.00% | 0.00% | FastAPI |

## Detailed Results

### FastAPI Results

#### 10 Concurrent Users
- **Throughput**: 292.41 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.026s
- **P95 Response Time**: 0.110s
- **P99 Response Time**: 0.129s
- **Avg CPU**: 90.1%
- **Avg Memory**: 61.7MB (max 62.1MB)

#### 20 Concurrent Users
- **Throughput**: 307.70 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.055s
- **P95 Response Time**: 0.234s
- **P99 Response Time**: 0.252s
- **Avg CPU**: 101.5%
- **Avg Memory**: 64.7MB (max 72.2MB)

#### 30 Concurrent Users
- **Throughput**: 331.34 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.079s
- **P95 Response Time**: 0.334s
- **P99 Response Time**: 0.352s
- **Avg CPU**: 101.4%
- **Avg Memory**: 72.8MB (max 73.0MB)

#### 40 Concurrent Users
- **Throughput**: 291.95 RPS
- **Error Rate**: 0.33%
- **Avg Response Time**: 0.118s
- **P95 Response Time**: 0.469s
- **P99 Response Time**: 0.834s
- **Avg CPU**: 99.9%
- **Avg Memory**: 83.5MB (max 93.9MB)

#### 50 Concurrent Users
- **Throughput**: 300.98 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.148s
- **P95 Response Time**: 0.625s
- **P99 Response Time**: 0.661s
- **Avg CPU**: 101.1%
- **Avg Memory**: 93.5MB (max 93.7MB)

#### 60 Concurrent Users
- **Throughput**: 296.43 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.182s
- **P95 Response Time**: 0.768s
- **P99 Response Time**: 0.823s
- **Avg CPU**: 99.7%
- **Avg Memory**: 93.8MB (max 93.9MB)

#### 70 Concurrent Users
- **Throughput**: 270.97 RPS
- **Error Rate**: 0.23%
- **Avg Response Time**: 0.235s
- **P95 Response Time**: 0.898s
- **P99 Response Time**: 1.269s
- **Avg CPU**: 95.5%
- **Avg Memory**: 100.2MB (max 108.5MB)

#### 80 Concurrent Users
- **Throughput**: 300.71 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.241s
- **P95 Response Time**: 1.022s
- **P99 Response Time**: 1.082s
- **Avg CPU**: 100.6%
- **Avg Memory**: 115.0MB (max 115.5MB)

#### 90 Concurrent Users
- **Throughput**: 295.91 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.275s
- **P95 Response Time**: 1.159s
- **P99 Response Time**: 1.270s
- **Avg CPU**: 101.3%
- **Avg Memory**: 115.7MB (max 115.9MB)

#### 100 Concurrent Users
- **Throughput**: 278.30 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.326s
- **P95 Response Time**: 1.442s
- **P99 Response Time**: 1.582s
- **Avg CPU**: 78.4%
- **Avg Memory**: 115.9MB (max 116.1MB)

### Django Results

#### 10 Concurrent Users
- **Throughput**: 71.91 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.123s
- **P95 Response Time**: 0.467s
- **P99 Response Time**: 0.566s
- **Avg CPU**: 99.1%
- **Avg Memory**: 60.5MB (max 65.3MB)

#### 20 Concurrent Users
- **Throughput**: 74.65 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.244s
- **P95 Response Time**: 0.696s
- **P99 Response Time**: 0.771s
- **Avg CPU**: 101.7%
- **Avg Memory**: 65.8MB (max 66.1MB)

#### 30 Concurrent Users
- **Throughput**: 74.25 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.363s
- **P95 Response Time**: 0.803s
- **P99 Response Time**: 0.910s
- **Avg CPU**: 79.5%
- **Avg Memory**: 65.5MB (max 66.0MB)

#### 40 Concurrent Users
- **Throughput**: 71.29 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.507s
- **P95 Response Time**: 0.922s
- **P99 Response Time**: 1.095s
- **Avg CPU**: 96.9%
- **Avg Memory**: 66.4MB (max 67.1MB)

#### 50 Concurrent Users
- **Throughput**: 73.59 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.608s
- **P95 Response Time**: 1.042s
- **P99 Response Time**: 1.202s
- **Avg CPU**: 101.4%
- **Avg Memory**: 66.4MB (max 66.8MB)

#### 60 Concurrent Users
- **Throughput**: 73.14 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.714s
- **P95 Response Time**: 1.207s
- **P99 Response Time**: 1.311s
- **Avg CPU**: 93.3%
- **Avg Memory**: 66.8MB (max 67.2MB)

#### 70 Concurrent Users
- **Throughput**: 75.64 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.813s
- **P95 Response Time**: 1.333s
- **P99 Response Time**: 1.547s
- **Avg CPU**: 88.9%
- **Avg Memory**: 72.1MB (max 72.5MB)

#### 80 Concurrent Users
- **Throughput**: 76.20 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.937s
- **P95 Response Time**: 1.417s
- **P99 Response Time**: 1.511s
- **Avg CPU**: 101.6%
- **Avg Memory**: 72.3MB (max 72.8MB)

#### 90 Concurrent Users
- **Throughput**: 75.98 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.061s
- **P95 Response Time**: 1.658s
- **P99 Response Time**: 2.000s
- **Avg CPU**: 87.5%
- **Avg Memory**: 72.6MB (max 73.1MB)

#### 100 Concurrent Users
- **Throughput**: 74.95 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.136s
- **P95 Response Time**: 1.746s
- **P99 Response Time**: 1.950s
- **Avg CPU**: 101.4%
- **Avg Memory**: 72.9MB (max 73.7MB)

## Analysis

### Performance Trends
- **FastAPI**: Shows async advantages at higher concurrency
- **Django**: Maintains consistent performance

### Breaking Points
- **FastAPI Breaking Point**: 100 users
- **Django Breaking Point**: 100 users

### Recommendations
- **For Low-Medium Concurrency**: Both frameworks perform well
- **For High Concurrency**: FastAPI shows better performance
- **For Reliability**: Django shows better error handling

---
*Report generated on: 2025-09-18 20:28:41*
