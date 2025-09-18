# Incremental Benchmark Report: FastAPI vs Django

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to 150 users
- **Step Size**: 50 users
- **Total Tests**: 3 concurrency levels

## Summary Results

| Concurrent Users | FastAPI Throughput | Django Throughput | FastAPI Error Rate | Django Error Rate | Winner |
|------------------|-------------------|-------------------|-------------------|-------------------|--------|
| 50 | 3.14 RPS | 5.19 RPS | 0.46% | 0.00% | Django |
| 100 | 3.13 RPS | 4.99 RPS | 11.88% | 3.75% | N/A (High Errors) |
| 150 | 2.92 RPS | 4.19 RPS | 52.17% | 38.33% | N/A (High Errors) |

## Detailed Results

### FastAPI Results

#### 50 Concurrent Users
- **Throughput**: 3.14 RPS
- **Error Rate**: 0.46%
- **Avg Response Time**: 12.125s
- **P95 Response Time**: 38.421s
- **P99 Response Time**: 57.127s

#### 100 Concurrent Users
- **Throughput**: 3.13 RPS
- **Error Rate**: 11.88%
- **Avg Response Time**: 26.305s
- **P95 Response Time**: 60.935s
- **P99 Response Time**: 60.998s

#### 150 Concurrent Users
- **Throughput**: 2.92 RPS
- **Error Rate**: 52.17%
- **Avg Response Time**: 44.322s
- **P95 Response Time**: 60.998s
- **P99 Response Time**: 61.000s

### Django Results

#### 50 Concurrent Users
- **Throughput**: 5.19 RPS
- **Error Rate**: 0.00%
- **Avg Response Time**: 8.992s
- **P95 Response Time**: 28.384s
- **P99 Response Time**: 31.491s

#### 100 Concurrent Users
- **Throughput**: 4.99 RPS
- **Error Rate**: 3.75%
- **Avg Response Time**: 18.669s
- **P95 Response Time**: 59.215s
- **P99 Response Time**: 60.418s

#### 150 Concurrent Users
- **Throughput**: 4.19 RPS
- **Error Rate**: 38.33%
- **Avg Response Time**: 33.687s
- **P95 Response Time**: 60.998s
- **P99 Response Time**: 60.999s

## Analysis

### Performance Trends
- **FastAPI**: Shows async advantages at higher concurrency
- **Django**: Maintains consistent performance

### Breaking Points
- **FastAPI Breaking Point**: 50 users
- **Django Breaking Point**: 100 users

### Recommendations
- **For Low-Medium Concurrency**: Both frameworks perform well
- **For High Concurrency**: Django shows better performance
- **For Reliability**: Django shows better error handling

---
*Report generated on: 2025-09-18 12:00:50*
