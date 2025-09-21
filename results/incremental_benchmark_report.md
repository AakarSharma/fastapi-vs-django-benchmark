# Incremental Benchmark Report: FastAPI vs Django WSGI vs Django ASGI

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 100 users
- **Step Size**: 50 users
- **Total Tests**: 10 concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ WSGI Thr (RPS) | DJ ASGI Thr (RPS) | FAPI Err % | DJ WSGI Err % | DJ ASGI Err % | Winner |
|-------------|----------------|-------------------|-------------------|------------|---------------|---------------|--------|
| 10 | 277.37 | 71.83 | 75.50 | 0.07% | 0.00% | 0.00% | FastAPI |
| 20 | 285.49 | 73.79 | 79.44 | 0.00% | 0.00% | 0.00% | FastAPI |
| 30 | 296.42 | 74.03 | 79.16 | 0.00% | 0.00% | 0.00% | FastAPI |
| 40 | 274.51 | 69.89 | 71.88 | 0.39% | 0.00% | 0.00% | FastAPI |
| 50 | 270.28 | 73.94 | 80.77 | 0.00% | 0.00% | 0.00% | FastAPI |
| 60 | 290.86 | 73.29 | 74.36 | 0.00% | 0.00% | 0.00% | FastAPI |
| 70 | 285.14 | 72.67 | 78.82 | 0.00% | 0.00% | 0.00% | FastAPI |
| 80 | 246.22 | 71.19 | 77.62 | 1.74% | 0.00% | 0.00% | FastAPI |
| 90 | 287.65 | 74.57 | 80.11 | 0.00% | 0.00% | 0.00% | FastAPI |
| 100 | 252.20 | 64.11 | 69.79 | 0.00% | 0.00% | 0.00% | FastAPI |

## Detailed Results

### FastAPI Results

#### 10 Concurrent Users
- **Throughput**: 277.37 RPS
- **Error Rate**: 0.07%
- **Avg Response Time**: 0.029s
- **P95 Response Time**: 0.119s
- **P99 Response Time**: 0.127s
- **Avg CPU**: 100.3%
- **Avg Memory**: 65.5MB (max 66.3MB)

#### 20 Concurrent Users
- **Throughput**: 285.49 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.060s
- **P95 Response Time**: 0.253s
- **P99 Response Time**: 0.282s
- **Avg CPU**: 101.1%
- **Avg Memory**: 68.8MB (max 68.9MB)

#### 30 Concurrent Users
- **Throughput**: 296.42 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.089s
- **P95 Response Time**: 0.375s
- **P99 Response Time**: 0.400s
- **Avg CPU**: 101.3%
- **Avg Memory**: 78.5MB (max 78.7MB)

#### 40 Concurrent Users
- **Throughput**: 274.51 RPS
- **Error Rate**: 0.39%
- **Avg Response Time**: 0.132s
- **P95 Response Time**: 0.513s
- **P99 Response Time**: 0.915s
- **Avg CPU**: 101.1%
- **Avg Memory**: 87.9MB (max 96.9MB)

#### 50 Concurrent Users
- **Throughput**: 270.28 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.168s
- **P95 Response Time**: 0.712s
- **P99 Response Time**: 0.770s
- **Avg CPU**: 81.5%
- **Avg Memory**: 96.8MB (max 97.0MB)

#### 60 Concurrent Users
- **Throughput**: 290.86 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.187s
- **P95 Response Time**: 0.786s
- **P99 Response Time**: 0.827s
- **Avg CPU**: 100.7%
- **Avg Memory**: 97.2MB (max 97.7MB)

#### 70 Concurrent Users
- **Throughput**: 285.14 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.224s
- **P95 Response Time**: 0.943s
- **P99 Response Time**: 0.983s
- **Avg CPU**: 101.8%
- **Avg Memory**: 97.6MB (max 97.8MB)

#### 80 Concurrent Users
- **Throughput**: 246.22 RPS
- **Error Rate**: 1.74%
- **Avg Response Time**: 0.289s
- **P95 Response Time**: 1.133s
- **P99 Response Time**: 1.777s
- **Avg CPU**: 81.3%
- **Avg Memory**: 115.5MB (max 120.0MB)

#### 90 Concurrent Users
- **Throughput**: 287.65 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.285s
- **P95 Response Time**: 1.199s
- **P99 Response Time**: 1.254s
- **Avg CPU**: 102.2%
- **Avg Memory**: 120.2MB (max 120.4MB)

#### 100 Concurrent Users
- **Throughput**: 252.20 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.358s
- **P95 Response Time**: 1.521s
- **P99 Response Time**: 1.596s
- **Avg CPU**: 83.4%
- **Avg Memory**: 120.5MB (max 120.7MB)

### Django WSGI Results

#### 10 Concurrent Users
- **Throughput**: 71.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.124s
- **P95 Response Time**: 0.467s
- **P99 Response Time**: 0.561s
- **Avg CPU**: 95.1%
- **Avg Memory**: 57.9MB (max 64.8MB)

#### 20 Concurrent Users
- **Throughput**: 73.79 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.250s
- **P95 Response Time**: 0.694s
- **P99 Response Time**: 0.784s
- **Avg CPU**: 101.7%
- **Avg Memory**: 71.5MB (max 71.7MB)

#### 30 Concurrent Users
- **Throughput**: 74.03 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.364s
- **P95 Response Time**: 0.792s
- **P99 Response Time**: 0.895s
- **Avg CPU**: 93.8%
- **Avg Memory**: 71.3MB (max 72.0MB)

#### 40 Concurrent Users
- **Throughput**: 69.89 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.512s
- **P95 Response Time**: 0.958s
- **P99 Response Time**: 1.130s
- **Avg CPU**: 102.0%
- **Avg Memory**: 71.7MB (max 72.0MB)

#### 50 Concurrent Users
- **Throughput**: 73.94 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.609s
- **P95 Response Time**: 1.141s
- **P99 Response Time**: 1.252s
- **Avg CPU**: 90.2%
- **Avg Memory**: 72.2MB (max 72.6MB)

#### 60 Concurrent Users
- **Throughput**: 73.29 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.710s
- **P95 Response Time**: 1.230s
- **P99 Response Time**: 1.471s
- **Avg CPU**: 98.6%
- **Avg Memory**: 72.1MB (max 72.6MB)

#### 70 Concurrent Users
- **Throughput**: 72.67 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.858s
- **P95 Response Time**: 1.382s
- **P99 Response Time**: 1.605s
- **Avg CPU**: 93.9%
- **Avg Memory**: 72.6MB (max 72.9MB)

#### 80 Concurrent Users
- **Throughput**: 71.19 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.005s
- **P95 Response Time**: 1.585s
- **P99 Response Time**: 1.812s
- **Avg CPU**: 93.4%
- **Avg Memory**: 72.7MB (max 73.4MB)

#### 90 Concurrent Users
- **Throughput**: 74.57 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.057s
- **P95 Response Time**: 1.596s
- **P99 Response Time**: 1.747s
- **Avg CPU**: 101.6%
- **Avg Memory**: 73.2MB (max 73.8MB)

#### 100 Concurrent Users
- **Throughput**: 64.11 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.395s
- **P95 Response Time**: 2.217s
- **P99 Response Time**: 2.446s
- **Avg CPU**: 101.8%
- **Avg Memory**: 73.5MB (max 74.0MB)

### Django ASGI Results

#### 10 Concurrent Users
- **Throughput**: 75.50 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.118s
- **P95 Response Time**: 0.442s
- **P99 Response Time**: 0.459s
- **Avg CPU**: 99.6%
- **Avg Memory**: 51.7MB (max 54.3MB)

#### 20 Concurrent Users
- **Throughput**: 79.44 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.228s
- **P95 Response Time**: 0.808s
- **P99 Response Time**: 0.842s
- **Avg CPU**: 103.9%
- **Avg Memory**: 58.4MB (max 62.0MB)

#### 30 Concurrent Users
- **Throughput**: 79.16 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.340s
- **P95 Response Time**: 1.192s
- **P99 Response Time**: 1.248s
- **Avg CPU**: 82.9%
- **Avg Memory**: 68.7MB (max 70.2MB)

#### 40 Concurrent Users
- **Throughput**: 71.88 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.505s
- **P95 Response Time**: 1.773s
- **P99 Response Time**: 1.884s
- **Avg CPU**: 94.9%
- **Avg Memory**: 74.2MB (max 76.2MB)

#### 50 Concurrent Users
- **Throughput**: 80.77 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.557s
- **P95 Response Time**: 1.973s
- **P99 Response Time**: 2.046s
- **Avg CPU**: 88.9%
- **Avg Memory**: 77.6MB (max 78.8MB)

#### 60 Concurrent Users
- **Throughput**: 74.36 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.711s
- **P95 Response Time**: 2.498s
- **P99 Response Time**: 2.701s
- **Avg CPU**: 82.9%
- **Avg Memory**: 80.5MB (max 81.9MB)

#### 70 Concurrent Users
- **Throughput**: 78.82 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.804s
- **P95 Response Time**: 2.799s
- **P99 Response Time**: 2.916s
- **Avg CPU**: 94.2%
- **Avg Memory**: 83.4MB (max 85.0MB)

#### 80 Concurrent Users
- **Throughput**: 77.62 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.935s
- **P95 Response Time**: 3.272s
- **P99 Response Time**: 3.481s
- **Avg CPU**: 103.6%
- **Avg Memory**: 87.0MB (max 88.4MB)

#### 90 Concurrent Users
- **Throughput**: 80.11 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.002s
- **P95 Response Time**: 3.519s
- **P99 Response Time**: 3.647s
- **Avg CPU**: 103.7%
- **Avg Memory**: 91.0MB (max 92.5MB)

#### 100 Concurrent Users
- **Throughput**: 69.79 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.293s
- **P95 Response Time**: 4.543s
- **P99 Response Time**: 4.679s
- **Avg CPU**: 94.1%
- **Avg Memory**: 92.9MB (max 94.5MB)

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
*Report generated on: 2025-09-22 00:03:56*
