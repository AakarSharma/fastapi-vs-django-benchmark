# Incremental Benchmark Report: FastAPI vs Django WSGI vs Django ASGI

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 100 users
- **Step Size**: 50 users
- **Total Tests**: 10 concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ WSGI Thr (RPS) | DJ ASGI Thr (RPS) | FAPI Err % | DJ WSGI Err % | DJ ASGI Err % | Winner |
|-------------|----------------|-------------------|-------------------|------------|---------------|---------------|--------|
| 10 | 270.79 | 72.90 | 49.16 | 0.04% | 0.00% | 0.00% | FastAPI |
| 20 | 286.27 | 72.83 | 49.21 | 0.00% | 0.00% | 0.00% | FastAPI |
| 30 | 296.99 | 72.48 | 49.61 | 0.00% | 0.00% | 0.00% | FastAPI |
| 40 | 270.86 | 74.10 | 48.42 | 0.18% | 0.00% | 0.00% | FastAPI |
| 50 | 289.15 | 74.12 | 49.58 | 0.00% | 0.00% | 0.00% | FastAPI |
| 60 | 292.44 | 74.02 | 48.70 | 0.00% | 0.00% | 0.00% | FastAPI |
| 70 | 281.42 | 73.83 | 48.79 | 0.00% | 0.00% | 0.00% | FastAPI |
| 80 | 250.20 | 74.21 | 49.07 | 2.11% | 0.00% | 0.00% | FastAPI |
| 90 | 280.89 | 74.00 | 49.49 | 0.00% | 0.00% | 0.00% | FastAPI |
| 100 | 273.82 | 74.11 | 49.52 | 0.00% | 0.00% | 0.00% | FastAPI |

## Detailed Results

### FastAPI Results

#### 10 Concurrent Users
- **Throughput**: 270.79 RPS
- **Error Rate**: 0.04%
- **Avg Response Time**: 0.028s
- **P95 Response Time**: 0.117s
- **P99 Response Time**: 0.127s
- **Avg CPU**: 90.9%
- **Avg Memory**: 62.8MB (max 63.2MB)

#### 20 Concurrent Users
- **Throughput**: 286.27 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.059s
- **P95 Response Time**: 0.249s
- **P99 Response Time**: 0.261s
- **Avg CPU**: 97.2%
- **Avg Memory**: 63.3MB (max 63.4MB)

#### 30 Concurrent Users
- **Throughput**: 296.99 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.088s
- **P95 Response Time**: 0.371s
- **P99 Response Time**: 0.391s
- **Avg CPU**: 99.0%
- **Avg Memory**: 73.6MB (max 73.8MB)

#### 40 Concurrent Users
- **Throughput**: 270.86 RPS
- **Error Rate**: 0.18%
- **Avg Response Time**: 0.127s
- **P95 Response Time**: 0.497s
- **P99 Response Time**: 0.950s
- **Avg CPU**: 101.5%
- **Avg Memory**: 85.7MB (max 94.1MB)

#### 50 Concurrent Users
- **Throughput**: 289.15 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.155s
- **P95 Response Time**: 0.650s
- **P99 Response Time**: 0.706s
- **Avg CPU**: 80.6%
- **Avg Memory**: 94.2MB (max 94.3MB)

#### 60 Concurrent Users
- **Throughput**: 292.44 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.186s
- **P95 Response Time**: 0.778s
- **P99 Response Time**: 0.817s
- **Avg CPU**: 101.7%
- **Avg Memory**: 94.6MB (max 94.7MB)

#### 70 Concurrent Users
- **Throughput**: 281.42 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.226s
- **P95 Response Time**: 0.947s
- **P99 Response Time**: 1.016s
- **Avg CPU**: 101.5%
- **Avg Memory**: 95.0MB (max 95.1MB)

#### 80 Concurrent Users
- **Throughput**: 250.20 RPS
- **Error Rate**: 2.11%
- **Avg Response Time**: 0.261s
- **P95 Response Time**: 1.015s
- **P99 Response Time**: 1.644s
- **Avg CPU**: 81.3%
- **Avg Memory**: 106.0MB (max 116.9MB)

#### 90 Concurrent Users
- **Throughput**: 280.89 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.291s
- **P95 Response Time**: 1.226s
- **P99 Response Time**: 1.289s
- **Avg CPU**: 81.5%
- **Avg Memory**: 120.5MB (max 120.6MB)

#### 100 Concurrent Users
- **Throughput**: 273.82 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.330s
- **P95 Response Time**: 1.409s
- **P99 Response Time**: 1.534s
- **Avg CPU**: 100.2%
- **Avg Memory**: 120.8MB (max 120.9MB)

### Django WSGI Results

#### 10 Concurrent Users
- **Throughput**: 72.90 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.121s
- **P95 Response Time**: 0.461s
- **P99 Response Time**: 0.533s
- **Avg CPU**: 96.6%
- **Avg Memory**: 59.7MB (max 64.8MB)

#### 20 Concurrent Users
- **Throughput**: 72.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.247s
- **P95 Response Time**: 0.669s
- **P99 Response Time**: 0.790s
- **Avg CPU**: 80.5%
- **Avg Memory**: 64.8MB (max 65.3MB)

#### 30 Concurrent Users
- **Throughput**: 72.48 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.372s
- **P95 Response Time**: 0.801s
- **P99 Response Time**: 0.880s
- **Avg CPU**: 88.5%
- **Avg Memory**: 65.1MB (max 65.6MB)

#### 40 Concurrent Users
- **Throughput**: 74.10 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.485s
- **P95 Response Time**: 0.888s
- **P99 Response Time**: 1.113s
- **Avg CPU**: 101.4%
- **Avg Memory**: 69.9MB (max 70.1MB)

#### 50 Concurrent Users
- **Throughput**: 74.12 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.597s
- **P95 Response Time**: 1.095s
- **P99 Response Time**: 1.271s
- **Avg CPU**: 91.6%
- **Avg Memory**: 70.2MB (max 70.5MB)

#### 60 Concurrent Users
- **Throughput**: 74.02 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.707s
- **P95 Response Time**: 1.173s
- **P99 Response Time**: 1.281s
- **Avg CPU**: 101.0%
- **Avg Memory**: 70.5MB (max 70.7MB)

#### 70 Concurrent Users
- **Throughput**: 73.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.856s
- **P95 Response Time**: 1.446s
- **P99 Response Time**: 1.691s
- **Avg CPU**: 88.1%
- **Avg Memory**: 70.4MB (max 70.9MB)

#### 80 Concurrent Users
- **Throughput**: 74.21 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.956s
- **P95 Response Time**: 1.466s
- **P99 Response Time**: 1.624s
- **Avg CPU**: 102.1%
- **Avg Memory**: 71.0MB (max 71.5MB)

#### 90 Concurrent Users
- **Throughput**: 74.00 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.051s
- **P95 Response Time**: 1.600s
- **P99 Response Time**: 1.692s
- **Avg CPU**: 86.5%
- **Avg Memory**: 71.1MB (max 71.7MB)

#### 100 Concurrent Users
- **Throughput**: 74.11 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.127s
- **P95 Response Time**: 1.733s
- **P99 Response Time**: 2.022s
- **Avg CPU**: 101.3%
- **Avg Memory**: 71.4MB (max 71.7MB)

### Django ASGI Results

#### 10 Concurrent Users
- **Throughput**: 49.16 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.184s
- **P95 Response Time**: 0.689s
- **P99 Response Time**: 0.722s
- **Avg CPU**: 100.9%
- **Avg Memory**: 60.6MB (max 64.2MB)

#### 20 Concurrent Users
- **Throughput**: 49.21 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.368s
- **P95 Response Time**: 1.229s
- **P99 Response Time**: 1.303s
- **Avg CPU**: 80.7%
- **Avg Memory**: 75.3MB (max 79.3MB)

#### 30 Concurrent Users
- **Throughput**: 49.61 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.548s
- **P95 Response Time**: 1.569s
- **P99 Response Time**: 1.645s
- **Avg CPU**: 85.7%
- **Avg Memory**: 89.2MB (max 92.3MB)

#### 40 Concurrent Users
- **Throughput**: 48.42 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.728s
- **P95 Response Time**: 1.852s
- **P99 Response Time**: 1.935s
- **Avg CPU**: 100.0%
- **Avg Memory**: 97.7MB (max 100.4MB)

#### 50 Concurrent Users
- **Throughput**: 49.58 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.904s
- **P95 Response Time**: 2.027s
- **P99 Response Time**: 2.284s
- **Avg CPU**: 102.0%
- **Avg Memory**: 106.9MB (max 109.7MB)

#### 60 Concurrent Users
- **Throughput**: 48.70 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.057s
- **P95 Response Time**: 2.334s
- **P99 Response Time**: 2.559s
- **Avg CPU**: 93.8%
- **Avg Memory**: 114.5MB (max 117.2MB)

#### 70 Concurrent Users
- **Throughput**: 48.79 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.251s
- **P95 Response Time**: 2.511s
- **P99 Response Time**: 2.742s
- **Avg CPU**: 100.7%
- **Avg Memory**: 123.5MB (max 128.0MB)

#### 80 Concurrent Users
- **Throughput**: 49.07 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.464s
- **P95 Response Time**: 2.836s
- **P99 Response Time**: 3.057s
- **Avg CPU**: 102.3%
- **Avg Memory**: 134.6MB (max 138.8MB)

#### 90 Concurrent Users
- **Throughput**: 49.49 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.623s
- **P95 Response Time**: 2.905s
- **P99 Response Time**: 3.357s
- **Avg CPU**: 98.8%
- **Avg Memory**: 140.6MB (max 143.5MB)

#### 100 Concurrent Users
- **Throughput**: 49.52 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.790s
- **P95 Response Time**: 3.074s
- **P99 Response Time**: 3.314s
- **Avg CPU**: 101.8%
- **Avg Memory**: 144.4MB (max 146.0MB)

## Analysis

### Performance Trends
- **FastAPI**: Shows async advantages at higher concurrency
- **Django WSGI**: Maintains consistent performance
- **Django ASGI**: Shows async advantages similar to FastAPI

### Breaking Points
- **FastAPI Breaking Point**: 100 users
- **Django WSGI Breaking Point**: 100 users
- **Django ASGI Breaking Point**: 100 users

### Recommendations
- **For Low-Medium Concurrency**: All frameworks perform well
- **For High Concurrency**: FastAPI shows better async performance
- **For Reliability**: Django WSGI shows better error handling
- **For Django Migration**: Django ASGI provides a good middle ground between Django WSGI and FastAPI

---
*Report generated on: 2025-09-18 23:33:25*
