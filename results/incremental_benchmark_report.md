# Incremental Benchmark Report: FastAPI vs Django WSGI vs Django ASGI

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 200 users
- **Step Size**: 50 users
- **Total Tests**: 26 concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ WSGI Thr (RPS) | DJ ASGI Thr (RPS) | FAPI Err % | DJ WSGI Err % | DJ ASGI Err % | Winner |
|-------------|----------------|-------------------|-------------------|------------|---------------|---------------|--------|
| 10 | 273.95 | 67.50 | 71.73 | 0.00% | 0.00% | 0.00% | FastAPI |
| 10 | 236.33 | 294.90 | 67.78 | 0.00% | 0.00% | 0.00% | Django WSGI |
| 20 | 73.37 | 284.24 | 301.42 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 30 | 68.08 | 76.31 | 284.48 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 40 | 301.33 | 67.84 | 74.46 | 0.00% | 0.00% | 0.00% | FastAPI |
| 40 | 291.37 | 259.11 | 67.97 | 0.00% | 1.03% | 0.00% | FastAPI |
| 50 | 75.88 | 254.14 | 265.45 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 60 | 69.66 | 75.98 | 272.57 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 70 | 269.87 | 68.58 | 75.44 | 0.00% | 0.00% | 0.00% | FastAPI |
| 70 | 265.98 | 265.37 | 68.83 | 0.00% | 0.00% | 0.00% | FastAPI |
| 80 | 74.65 | 268.30 | 264.37 | 0.00% | 0.00% | 0.00% | Django WSGI |
| 90 | 68.41 | 75.19 | 264.58 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 100 | 209.36 | 68.71 | 70.26 | 5.55% | 0.00% | 0.00% | FastAPI |
| 100 | 206.77 | 277.82 | 71.41 | 0.00% | 0.00% | 0.00% | Django WSGI |
| 110 | 79.00 | 234.12 | 277.45 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 120 | 71.48 | 72.93 | 190.06 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 130 | 259.15 | 69.16 | 71.83 | 0.00% | 0.00% | 0.00% | FastAPI |
| 130 | 200.51 | 221.77 | 61.11 | 0.00% | 0.59% | 0.00% | Django WSGI |
| 140 | 75.84 | 225.17 | 259.22 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 150 | 66.16 | 75.57 | 221.66 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 160 | 256.91 | 68.64 | 75.10 | 0.00% | 0.00% | 0.00% | FastAPI |
| 160 | 172.76 | 303.18 | 72.10 | 0.00% | 0.00% | 0.00% | Django WSGI |
| 170 | 79.80 | 160.16 | 266.03 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 180 | 73.04 | 70.92 | 154.78 | 0.00% | 0.00% | 0.00% | Django ASGI |
| 190 | 152.82 | 73.77 | 80.94 | 0.00% | 0.00% | 0.00% | FastAPI |
| 190 | 155.83 | 133.33 | 74.07 | 0.00% | 0.00% | 0.00% | FastAPI |

## Detailed Results

### FastAPI Results

#### 10 Concurrent Users
- **Throughput**: 273.95 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.029s
- **P95 Response Time**: 0.119s
- **P99 Response Time**: 0.131s
- **Avg CPU**: 84.5%
- **Avg Memory**: 62.1MB (max 62.3MB)

#### 20 Concurrent Users
- **Throughput**: 294.90 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.058s
- **P95 Response Time**: 0.243s
- **P99 Response Time**: 0.253s
- **Avg CPU**: 77.5%
- **Avg Memory**: 62.4MB (max 62.5MB)

#### 30 Concurrent Users
- **Throughput**: 301.42 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.086s
- **P95 Response Time**: 0.365s
- **P99 Response Time**: 0.390s
- **Avg CPU**: 76.8%
- **Avg Memory**: 73.1MB (max 73.3MB)

#### 40 Concurrent Users
- **Throughput**: 301.33 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.119s
- **P95 Response Time**: 0.500s
- **P99 Response Time**: 0.525s
- **Avg CPU**: 78.6%
- **Avg Memory**: 73.8MB (max 74.3MB)

#### 50 Concurrent Users
- **Throughput**: 259.11 RPS
- **Error Rate**: 1.03%
- **Avg Response Time**: 0.176s
- **P95 Response Time**: 0.677s
- **P99 Response Time**: 1.163s
- **Avg CPU**: 101.3%
- **Avg Memory**: 85.3MB (max 99.8MB)

#### 60 Concurrent Users
- **Throughput**: 265.45 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.202s
- **P95 Response Time**: 0.863s
- **P99 Response Time**: 0.965s
- **Avg CPU**: 88.4%
- **Avg Memory**: 100.0MB (max 100.3MB)

#### 70 Concurrent Users
- **Throughput**: 269.87 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.234s
- **P95 Response Time**: 0.986s
- **P99 Response Time**: 1.034s
- **Avg CPU**: 86.6%
- **Avg Memory**: 100.3MB (max 100.6MB)

#### 80 Concurrent Users
- **Throughput**: 265.37 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.273s
- **P95 Response Time**: 1.164s
- **P99 Response Time**: 1.236s
- **Avg CPU**: 85.8%
- **Avg Memory**: 100.6MB (max 100.8MB)

#### 90 Concurrent Users
- **Throughput**: 264.37 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.308s
- **P95 Response Time**: 1.296s
- **P99 Response Time**: 1.356s
- **Avg CPU**: 89.0%
- **Avg Memory**: 100.8MB (max 101.0MB)

#### 100 Concurrent Users
- **Throughput**: 209.36 RPS
- **Error Rate**: 5.55%
- **Avg Response Time**: 0.431s
- **P95 Response Time**: 1.925s
- **P99 Response Time**: 2.234s
- **Avg CPU**: 80.1%
- **Avg Memory**: 116.8MB (max 127.9MB)

#### 110 Concurrent Users
- **Throughput**: 277.82 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.359s
- **P95 Response Time**: 1.357s
- **P99 Response Time**: 1.394s
- **Avg CPU**: 88.1%
- **Avg Memory**: 127.9MB (max 127.9MB)

#### 120 Concurrent Users
- **Throughput**: 277.45 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.395s
- **P95 Response Time**: 1.485s
- **P99 Response Time**: 1.513s
- **Avg CPU**: 94.8%
- **Avg Memory**: 128.1MB (max 128.2MB)

#### 130 Concurrent Users
- **Throughput**: 259.15 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.452s
- **P95 Response Time**: 1.703s
- **P99 Response Time**: 1.787s
- **Avg CPU**: 91.7%
- **Avg Memory**: 128.6MB (max 128.8MB)

#### 140 Concurrent Users
- **Throughput**: 221.77 RPS
- **Error Rate**: 0.59%
- **Avg Response Time**: 0.556s
- **P95 Response Time**: 1.803s
- **P99 Response Time**: 2.300s
- **Avg CPU**: 80.1%
- **Avg Memory**: 124.6MB (max 131.6MB)

#### 150 Concurrent Users
- **Throughput**: 259.22 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.530s
- **P95 Response Time**: 2.034s
- **P99 Response Time**: 2.205s
- **Avg CPU**: 100.8%
- **Avg Memory**: 132.5MB (max 132.6MB)

#### 160 Concurrent Users
- **Throughput**: 256.91 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.579s
- **P95 Response Time**: 2.104s
- **P99 Response Time**: 2.192s
- **Avg CPU**: 101.1%
- **Avg Memory**: 132.9MB (max 133.0MB)

#### 170 Concurrent Users
- **Throughput**: 303.18 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.511s
- **P95 Response Time**: 1.915s
- **P99 Response Time**: 1.971s
- **Avg CPU**: 99.2%
- **Avg Memory**: 133.3MB (max 133.4MB)

#### 180 Concurrent Users
- **Throughput**: 266.03 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.569s
- **P95 Response Time**: 1.980s
- **P99 Response Time**: 2.046s
- **Avg CPU**: 81.0%
- **Avg Memory**: 129.7MB (max 134.1MB)

#### 190 Concurrent Users
- **Throughput**: 152.82 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.118s
- **P95 Response Time**: 5.856s
- **P99 Response Time**: 6.833s
- **Avg CPU**: 63.0%
- **Avg Memory**: 116.7MB (max 117.1MB)

#### 200 Concurrent Users
- **Throughput**: 133.33 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.327s
- **P95 Response Time**: 6.614s
- **P99 Response Time**: 7.497s
- **Avg CPU**: 59.9%
- **Avg Memory**: 117.3MB (max 117.6MB)

### Django WSGI Results

#### 10 Concurrent Users
- **Throughput**: 67.50 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.133s
- **P95 Response Time**: 0.497s
- **P99 Response Time**: 0.568s
- **Avg CPU**: 102.0%
- **Avg Memory**: 60.6MB (max 66.7MB)

#### 20 Concurrent Users
- **Throughput**: 67.78 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.262s
- **P95 Response Time**: 0.688s
- **P99 Response Time**: 0.772s
- **Avg CPU**: 86.2%
- **Avg Memory**: 66.9MB (max 67.6MB)

#### 30 Concurrent Users
- **Throughput**: 68.08 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.391s
- **P95 Response Time**: 0.884s
- **P99 Response Time**: 0.953s
- **Avg CPU**: 100.6%
- **Avg Memory**: 67.5MB (max 67.8MB)

#### 40 Concurrent Users
- **Throughput**: 67.84 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.524s
- **P95 Response Time**: 1.030s
- **P99 Response Time**: 1.262s
- **Avg CPU**: 96.9%
- **Avg Memory**: 67.5MB (max 68.3MB)

#### 50 Concurrent Users
- **Throughput**: 67.97 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.639s
- **P95 Response Time**: 1.135s
- **P99 Response Time**: 1.338s
- **Avg CPU**: 101.9%
- **Avg Memory**: 72.7MB (max 73.0MB)

#### 60 Concurrent Users
- **Throughput**: 69.66 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.768s
- **P95 Response Time**: 1.322s
- **P99 Response Time**: 1.374s
- **Avg CPU**: 101.0%
- **Avg Memory**: 73.0MB (max 73.2MB)

#### 70 Concurrent Users
- **Throughput**: 68.58 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.863s
- **P95 Response Time**: 1.524s
- **P99 Response Time**: 1.792s
- **Avg CPU**: 100.7%
- **Avg Memory**: 72.9MB (max 73.7MB)

#### 80 Concurrent Users
- **Throughput**: 68.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.010s
- **P95 Response Time**: 1.609s
- **P99 Response Time**: 1.706s
- **Avg CPU**: 100.7%
- **Avg Memory**: 73.6MB (max 74.1MB)

#### 90 Concurrent Users
- **Throughput**: 68.41 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.137s
- **P95 Response Time**: 1.774s
- **P99 Response Time**: 1.879s
- **Avg CPU**: 87.4%
- **Avg Memory**: 73.7MB (max 74.3MB)

#### 100 Concurrent Users
- **Throughput**: 68.71 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.266s
- **P95 Response Time**: 1.950s
- **P99 Response Time**: 2.186s
- **Avg CPU**: 98.4%
- **Avg Memory**: 71.9MB (max 72.4MB)

#### 110 Concurrent Users
- **Throughput**: 71.41 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.350s
- **P95 Response Time**: 1.894s
- **P99 Response Time**: 2.099s
- **Avg CPU**: 101.3%
- **Avg Memory**: 72.1MB (max 72.5MB)

#### 120 Concurrent Users
- **Throughput**: 71.48 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.502s
- **P95 Response Time**: 2.179s
- **P99 Response Time**: 2.517s
- **Avg CPU**: 86.9%
- **Avg Memory**: 72.2MB (max 73.1MB)

#### 130 Concurrent Users
- **Throughput**: 69.16 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.601s
- **P95 Response Time**: 2.458s
- **P99 Response Time**: 2.802s
- **Avg CPU**: 93.6%
- **Avg Memory**: 72.6MB (max 73.4MB)

#### 140 Concurrent Users
- **Throughput**: 61.11 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.657s
- **P95 Response Time**: 2.350s
- **P99 Response Time**: 2.656s
- **Avg CPU**: 85.0%
- **Avg Memory**: 67.4MB (max 73.4MB)

#### 150 Concurrent Users
- **Throughput**: 66.16 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.758s
- **P95 Response Time**: 2.792s
- **P99 Response Time**: 3.198s
- **Avg CPU**: 102.2%
- **Avg Memory**: 62.5MB (max 67.9MB)

#### 160 Concurrent Users
- **Throughput**: 68.64 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.796s
- **P95 Response Time**: 2.669s
- **P99 Response Time**: 2.918s
- **Avg CPU**: 102.4%
- **Avg Memory**: 67.9MB (max 68.5MB)

#### 170 Concurrent Users
- **Throughput**: 72.10 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.801s
- **P95 Response Time**: 2.647s
- **P99 Response Time**: 2.895s
- **Avg CPU**: 101.8%
- **Avg Memory**: 68.3MB (max 68.7MB)

#### 180 Concurrent Users
- **Throughput**: 73.04 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.904s
- **P95 Response Time**: 2.808s
- **P99 Response Time**: 2.989s
- **Avg CPU**: 98.2%
- **Avg Memory**: 68.7MB (max 69.8MB)

#### 190 Concurrent Users
- **Throughput**: 73.77 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 2.015s
- **P95 Response Time**: 3.110s
- **P99 Response Time**: 3.337s
- **Avg CPU**: 101.5%
- **Avg Memory**: 68.8MB (max 69.6MB)

#### 200 Concurrent Users
- **Throughput**: 74.07 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 2.132s
- **P95 Response Time**: 3.193s
- **P99 Response Time**: 3.334s
- **Avg CPU**: 101.6%
- **Avg Memory**: 69.3MB (max 70.2MB)

### Django ASGI Results

#### 10 Concurrent Users
- **Throughput**: 71.73 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.124s
- **P95 Response Time**: 0.455s
- **P99 Response Time**: 0.471s
- **Avg CPU**: 78.5%
- **Avg Memory**: 51.0MB (max 52.4MB)

#### 20 Concurrent Users
- **Throughput**: 73.37 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.243s
- **P95 Response Time**: 0.866s
- **P99 Response Time**: 0.920s
- **Avg CPU**: 100.1%
- **Avg Memory**: 55.8MB (max 56.7MB)

#### 30 Concurrent Users
- **Throughput**: 76.31 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.352s
- **P95 Response Time**: 1.247s
- **P99 Response Time**: 1.279s
- **Avg CPU**: 98.1%
- **Avg Memory**: 67.0MB (max 70.4MB)

#### 40 Concurrent Users
- **Throughput**: 74.46 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.485s
- **P95 Response Time**: 1.723s
- **P99 Response Time**: 1.827s
- **Avg CPU**: 102.6%
- **Avg Memory**: 74.3MB (max 75.1MB)

#### 50 Concurrent Users
- **Throughput**: 75.88 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.585s
- **P95 Response Time**: 2.083s
- **P99 Response Time**: 2.171s
- **Avg CPU**: 100.4%
- **Avg Memory**: 76.6MB (max 77.9MB)

#### 60 Concurrent Users
- **Throughput**: 75.98 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.722s
- **P95 Response Time**: 2.497s
- **P99 Response Time**: 2.564s
- **Avg CPU**: 99.5%
- **Avg Memory**: 79.5MB (max 80.6MB)

#### 70 Concurrent Users
- **Throughput**: 75.44 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.808s
- **P95 Response Time**: 2.944s
- **P99 Response Time**: 3.010s
- **Avg CPU**: 103.3%
- **Avg Memory**: 83.7MB (max 84.4MB)

#### 80 Concurrent Users
- **Throughput**: 74.65 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 0.952s
- **P95 Response Time**: 3.396s
- **P99 Response Time**: 3.503s
- **Avg CPU**: 103.8%
- **Avg Memory**: 85.9MB (max 87.2MB)

#### 90 Concurrent Users
- **Throughput**: 75.19 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.075s
- **P95 Response Time**: 3.736s
- **P99 Response Time**: 3.813s
- **Avg CPU**: 103.4%
- **Avg Memory**: 89.5MB (max 90.6MB)

#### 100 Concurrent Users
- **Throughput**: 70.26 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.292s
- **P95 Response Time**: 4.452s
- **P99 Response Time**: 4.554s
- **Avg CPU**: 82.6%
- **Avg Memory**: 91.4MB (max 93.0MB)

#### 110 Concurrent Users
- **Throughput**: 79.00 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.256s
- **P95 Response Time**: 4.331s
- **P99 Response Time**: 4.487s
- **Avg CPU**: 88.7%
- **Avg Memory**: 94.2MB (max 96.5MB)

#### 120 Concurrent Users
- **Throughput**: 72.93 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.497s
- **P95 Response Time**: 5.432s
- **P99 Response Time**: 5.583s
- **Avg CPU**: 103.4%
- **Avg Memory**: 98.4MB (max 99.2MB)

#### 130 Concurrent Users
- **Throughput**: 71.83 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.566s
- **P95 Response Time**: 5.786s
- **P99 Response Time**: 5.981s
- **Avg CPU**: 103.6%
- **Avg Memory**: 101.3MB (max 102.9MB)

#### 140 Concurrent Users
- **Throughput**: 75.84 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.521s
- **P95 Response Time**: 5.901s
- **P99 Response Time**: 6.116s
- **Avg CPU**: 103.4%
- **Avg Memory**: 103.7MB (max 105.4MB)

#### 150 Concurrent Users
- **Throughput**: 75.57 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.608s
- **P95 Response Time**: 6.388s
- **P99 Response Time**: 6.603s
- **Avg CPU**: 103.4%
- **Avg Memory**: 106.4MB (max 108.9MB)

#### 160 Concurrent Users
- **Throughput**: 75.10 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.782s
- **P95 Response Time**: 6.871s
- **P99 Response Time**: 7.058s
- **Avg CPU**: 103.5%
- **Avg Memory**: 108.7MB (max 110.4MB)

#### 170 Concurrent Users
- **Throughput**: 79.80 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 1.769s
- **P95 Response Time**: 6.811s
- **P99 Response Time**: 7.042s
- **Avg CPU**: 103.7%
- **Avg Memory**: 114.1MB (max 116.8MB)

#### 180 Concurrent Users
- **Throughput**: 70.92 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 2.228s
- **P95 Response Time**: 7.927s
- **P99 Response Time**: 8.394s
- **Avg CPU**: 86.8%
- **Avg Memory**: 118.8MB (max 122.6MB)

#### 190 Concurrent Users
- **Throughput**: 80.94 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 2.014s
- **P95 Response Time**: 7.564s
- **P99 Response Time**: 7.731s
- **Avg CPU**: 103.0%
- **Avg Memory**: 125.8MB (max 127.5MB)

#### 200 Concurrent Users
- **Throughput**: 76.62 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 2.296s
- **P95 Response Time**: 8.347s
- **P99 Response Time**: 8.720s
- **Avg CPU**: 93.8%
- **Avg Memory**: 127.4MB (max 131.4MB)

## Analysis

### Performance Trends
- **FastAPI**: Shows async advantages at higher concurrency
- **Django WSGI**: Maintains consistent performance
- **Django ASGI**: Shows async advantages similar to FastAPI

### Breaking Points
- **FastAPI Breaking Point**: 200 users
- **Django WSGI Breaking Point**: 200 users
- **Django ASGI Breaking Point**: 200 users

### Recommendations
- **For Low-Medium Concurrency**: All frameworks perform well
- **For High Concurrency**: FastAPI shows better async performance
- **For Reliability**: Django WSGI shows better error handling
- **For Django Migration**: Django ASGI provides a good middle ground between Django WSGI and FastAPI

---
*Report generated on: 2025-09-22 16:13:05*
