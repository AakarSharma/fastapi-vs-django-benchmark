#!/usr/bin/env python3
"""
Simple Incremental Benchmark Script for FastAPI vs Django
Tests both frameworks with increasing concurrency levels from 50 to 1000 users
"""

import asyncio
import aiohttp
import time
import json
import argparse
from typing import Dict, List, Tuple
import statistics
import traceback
from datetime import datetime
import asyncio.subprocess as asp
import re
import random

class SimpleIncrementalBenchmark:
    def __init__(self, fastapi_url: str, django_url: str):
        self.fastapi_url = fastapi_url
        self.django_url = django_url
        self.results = []
        # Container identifiers will be resolved dynamically via `docker compose ps -q`

    @staticmethod
    def _parse_cpu_percent(s: str) -> float:
        try:
            return float(s.strip().replace('%', ''))
        except Exception:
            return 0.0

    @staticmethod
    def _parse_mem_usage_mb(s: str) -> float:
        # e.g. "156.5MiB / 2.00GiB"
        try:
            first = s.split('/')[0].strip()
            value_str, unit = re.match(r"([0-9.]+)([KMG]i?B)", first).groups()
            value = float(value_str)
            unit = unit.lower()
            if unit in ("kb", "kib"):
                return value / 1024.0
            if unit in ("mb", "mib"):
                return value
            if unit in ("gb", "gib"):
                return value * 1024.0
            return value
        except Exception:
            return 0.0

    async def _sample_container_stats(self, container_name: str, stop_event: asyncio.Event, samples: list):
        fmt = "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"
        while not stop_event.is_set():
            try:
                proc = await asp.create_subprocess_exec(
                    "docker", "stats", "--no-stream", "--format", fmt, container_name,
                    stdout=asp.PIPE, stderr=asp.PIPE,
                )
                stdout, _ = await proc.communicate()
                line = stdout.decode().strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        cpu = self._parse_cpu_percent(parts[1])
                        mem_mb = self._parse_mem_usage_mb(parts[2])
                        samples.append((cpu, mem_mb))
            except Exception:
                # Ignore sampling errors, keep going
                pass
            await asyncio.sleep(1.0)

    async def _resolve_container_identifier(self, service_name: str) -> str:
        """Return the container ID for a given compose service, or empty string if not found."""
        try:
            proc = await asp.create_subprocess_exec(
                "docker", "compose", "-f", "docker-compose.yml", "ps", "-q", service_name,
                stdout=asp.PIPE, stderr=asp.PIPE,
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        except Exception:
            return ""
        
    async def test_endpoint(self, session: aiohttp.ClientSession, url: str, endpoint: str, method: str = "GET", data: dict = None, worker_id: int = -1) -> Tuple[float, int, bool, dict | None]:
        """Test a single endpoint and return (response_time, status_code, success, error_info)"""
        start_time = time.time()
        try:
            if method == "POST":
                async with session.post(f"{url}{endpoint}", json=data, timeout=300) as response:
                    body = await response.text()
                    success = response.status == 200
                    if not success:
                        return (
                            time.time() - start_time,
                            response.status,
                            False,
                            {
                                "when": datetime.utcnow().isoformat() + "Z",
                                "endpoint": endpoint,
                                "method": method,
                                "status_code": response.status,
                                "response_body": body[:500],
                                "error_type": "HTTP_NON_200",
                                "error_message": f"Non-200 response ({response.status})",
                                "worker_id": worker_id,
                                "client_timeout_s": 300,
                            },
                        )
                    return time.time() - start_time, response.status, True, None
            else:
                async with session.get(f"{url}{endpoint}", timeout=300) as response:
                    body = await response.text()
                    success = response.status == 200
                    if not success:
                        return (
                            time.time() - start_time,
                            response.status,
                            False,
                            {
                                "when": datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                                "endpoint": endpoint,
                                "method": method,
                                "status_code": response.status,
                                "response_body": body[:500],
                                "error_type": "HTTP_NON_200",
                                "error_message": f"Non-200 response ({response.status})",
                                "worker_id": worker_id,
                                "client_timeout_s": 300,
                            },
                        )
                    return time.time() - start_time, response.status, True, None
        except Exception as e:
            return (
                time.time() - start_time,
                500,
                False,
                {
                    "when": datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": 500,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "traceback": traceback.format_exc()[-4000:],
                    "worker_id": worker_id,
                    "client_timeout_s": 60,
                },
            )

    async def run_load_test(self, url: str, framework: str, duration: int, concurrent: int) -> Dict:
        """Run load test for a specific framework"""
        print(f"Starting {framework} load test for {duration} seconds with {concurrent} concurrent users...")
        
        endpoints = [
            ("/api/benchmark/io_intensive/", "POST", {}) if framework == "django" else ("/io-intensive", "POST", {}),
            ("/api/users/", "GET", None) if framework == "django" else ("/users", "GET", None),
            ("/api/products/", "GET", None) if framework == "django" else ("/products", "GET", None),
            ("/api/orders/", "GET", None) if framework == "django" else ("/orders", "GET", None),
        ]
        
        connector = aiohttp.TCPConnector(limit=2000, limit_per_host=1000, keepalive_timeout=30)
        timeout = aiohttp.ClientTimeout(total=60)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Health check first
            health_endpoint = "/api/benchmark/health/" if framework == "django" else "/health"
            try:
                async with session.get(f"{url}{health_endpoint}", timeout=10) as response:
                    if response.status != 200:
                        print(f"Health check failed for {framework}: {response.status}")
                        return None
            except Exception as e:
                print(f"Health check failed for {framework}: {e}")
                return None
            
            start_time = time.time()
            response_times = []
            status_codes = []
            errors = []
            error_details: List[dict] = []

            # Start docker stats sampler for this framework's container (resolve dynamically)
            container_name = await self._resolve_container_identifier(framework)
            stats_samples: List[tuple] = []
            stop_event = asyncio.Event()
            sampler_task = None
            if container_name:
                sampler_task = asyncio.create_task(self._sample_container_stats(container_name, stop_event, stats_samples))
            
            # Create tasks for concurrent requests
            tasks = []
            for i in range(concurrent):
                task = self.worker_task(session, url, endpoints, duration, i)
                tasks.append(task)
            
            # Run all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect results from all tasks
            for result in results:
                if isinstance(result, dict):
                    response_times.extend(result.get('response_times', []))
                    status_codes.extend(result.get('status_codes', []))
                    errors.extend(result.get('errors', []))
                    error_details.extend(result.get('error_details', []))
            
            end_time = time.time()
            total_duration = end_time - start_time

            # Stop sampler and compute CPU/memory stats
            if container_name and sampler_task:
                stop_event.set()
                try:
                    await sampler_task
                except Exception:
                    pass
            if stats_samples:
                cpu_values = [c for c, _ in stats_samples]
                mem_values = [m for _, m in stats_samples]
                avg_cpu = sum(cpu_values) / len(cpu_values)
                avg_mem = sum(mem_values) / len(mem_values)
                max_mem = max(mem_values)
            else:
                avg_cpu = 0.0
                avg_mem = 0.0
                max_mem = 0.0
            
            total_requests = len(response_times)
            successful_requests = len([s for s in status_codes if s == 200])
            error_requests = len([s for s in status_codes if s != 200])
            error_rate = (error_requests / total_requests * 100) if total_requests > 0 else 0
            
            throughput = total_requests / total_duration if total_duration > 0 else 0
            
            if response_times:
                response_times.sort()
                avg_response_time = statistics.mean(response_times)
                p95_response_time = response_times[int(len(response_times) * 0.95)] if len(response_times) > 0 else 0
                p99_response_time = response_times[int(len(response_times) * 0.99)] if len(response_times) > 0 else 0
            else:
                avg_response_time = p95_response_time = p99_response_time = 0
            
            result = {
                "framework": framework,
                "concurrent_users": concurrent,
                "duration": total_duration,
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "error_requests": error_requests,
                "error_rate": error_rate,
                "throughput": throughput,
                "avg_response_time": avg_response_time,
                "p95_response_time": p95_response_time,
                "p99_response_time": p99_response_time,
                "avg_cpu_percent": round(avg_cpu, 2),
                "avg_memory_mb": round(avg_mem, 1),
                "max_memory_mb": round(max_mem, 1),
                "errors": error_details[:10] if error_details else errors[:10]
            }
            
            print(f"{framework} Results:")
            print(f"  Total Requests: {total_requests}")
            print(f"  Duration: {total_duration:.2f}s")
            print(f"  Throughput: {throughput:.2f} RPS")
            print(f"  Avg Response Time: {avg_response_time:.3f}s")
            print(f"  P95 Response Time: {p95_response_time:.3f}s")
            print(f"  P99 Response Time: {p99_response_time:.3f}s")
            print(f"  Error Rate: {error_rate:.2f}%")
            print(f"  Avg CPU: {avg_cpu:.1f}%")
            print(f"  Avg Memory: {avg_mem:.1f}MB (max {max_mem:.1f}MB)")
            print()
            
            return result

    async def worker_task(self, session: aiohttp.ClientSession, url: str, endpoints: List, duration: int, worker_id: int):
        """Worker task that makes requests for the specified duration"""
        response_times = []
        status_codes = []
        errors = []
        error_details: List[dict] = []
        
        end_time = time.time() + duration
        
        # Initial stagger to avoid synchronized start bursts across workers
        try:
            initial_delay = random.uniform(0.0, min(1.0, duration * 0.1))
            if initial_delay > 0:
                await asyncio.sleep(initial_delay)
        except Exception:
            pass
        
        while time.time() < end_time:
            # Shuffle endpoint order each cycle to avoid phase alignment
            for endpoint, method, data in random.sample(endpoints, k=len(endpoints)):
                response_time, status_code, success, err = await self.test_endpoint(session, url, endpoint, method, data, worker_id)
                response_times.append(response_time)
                status_codes.append(status_code)
                
                if not success:
                    # Keep a simple string plus a detailed record
                    errors.append(f"{endpoint}: {status_code}")
                    if err:
                        error_details.append(err)
                
                # Small jitter between requests to prevent synchronized pacing
                try:
                    await asyncio.sleep(random.uniform(0.001, 0.01))
                except Exception:
                    pass
        
        return {
            'response_times': response_times,
            'status_codes': status_codes,
            'errors': errors,
            'error_details': error_details,
        }

    async def run_incremental_benchmark(self, max_concurrent: int = 1000, step: int = 50, duration: int = 30):
        """Run incremental benchmark from 50 to max_concurrent users"""
        print(f"Starting Incremental Benchmark: {step} to {max_concurrent} concurrent users")
        print(f"Duration per test: {duration} seconds")
        print("=" * 80)
        
        concurrent_levels = list(range(step, max_concurrent + 1, step))
        
        for concurrent in concurrent_levels:
            print(f"\n{'='*20} TESTING {concurrent} CONCURRENT USERS {'='*20}")
            
            # Test FastAPI
            fastapi_result = await self.run_load_test(self.fastapi_url, "fastapi", duration, concurrent)
            if fastapi_result:
                self.results.append(fastapi_result)
            
            print("Waiting 10 seconds before testing Django...")
            await asyncio.sleep(10)
            
            # Test Django
            django_result = await self.run_load_test(self.django_url, "django", duration, concurrent)
            if django_result:
                self.results.append(django_result)
            
            print("Waiting 15 seconds before next test...")
            await asyncio.sleep(15)
            
            # Check if we should stop due to high error rates
            if fastapi_result and django_result:
                if fastapi_result["error_rate"] > 50 or django_result["error_rate"] > 50:
                    print(f"Stopping benchmark due to high error rates at {concurrent} concurrent users")
                    break

    def save_results(self, filename: str = "incremental_benchmark_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")

    def generate_report(self, filename: str = "incremental_benchmark_report.md"):
        """Generate a comprehensive markdown report"""
        if not self.results:
            print("No results to generate report")
            return
        
        fastapi_results = [r for r in self.results if r["framework"] == "fastapi"]
        django_results = [r for r in self.results if r["framework"] == "django"]
        
        report = f"""# Incremental Benchmark Report: FastAPI vs Django

## Test Configuration
- **Test Duration**: 30 seconds per concurrency level
- **Concurrency Range**: 50 to {max([r['concurrent_users'] for r in self.results])} users
- **Step Size**: 50 users
- **Total Tests**: {len(self.results) // 2} concurrency levels

## Summary Results

| Concurrency | FAPI Thr (RPS) | DJ Thr (RPS) | FAPI Err % | DJ Err % | Winner |
|-------------|----------------|--------------|------------|----------|--------|
"""
        
        for i in range(0, len(self.results), 2):
            if i + 1 < len(self.results):
                fastapi = self.results[i]
                django = self.results[i + 1]
                
                winner = "FastAPI" if fastapi["throughput"] > django["throughput"] else "Django"
                if fastapi["error_rate"] > 10 or django["error_rate"] > 10:
                    winner = "N/A (High Errors)"
                
                report += f"| {fastapi['concurrent_users']} | {fastapi['throughput']:.2f} | {django['throughput']:.2f} | {fastapi['error_rate']:.2f}% | {django['error_rate']:.2f}% | {winner} |\n"
        
        report += f"""
## Detailed Results

### FastAPI Results
"""
        
        for result in fastapi_results:
            report += f"""
#### {result['concurrent_users']} Concurrent Users
- **Throughput**: {result['throughput']:.2f} RPS
- **Error Rate**: {result['error_rate']:.2f}%
- **Avg Response Time**: {result['avg_response_time']:.3f}s
- **P95 Response Time**: {result['p95_response_time']:.3f}s
- **P99 Response Time**: {result['p99_response_time']:.3f}s
- **Avg CPU**: {result.get('avg_cpu_percent', 0):.1f}%
- **Avg Memory**: {result.get('avg_memory_mb', 0):.1f}MB (max {result.get('max_memory_mb', 0):.1f}MB)
"""
        
        report += f"""
### Django Results
"""
        
        for result in django_results:
            report += f"""
#### {result['concurrent_users']} Concurrent Users
- **Throughput**: {result['throughput']:.2f} RPS
- **Error Rate**: {result['error_rate']:.2f}%
- **Avg Response Time**: {result['avg_response_time']:.3f}s
- **P95 Response Time**: {result['p95_response_time']:.3f}s
- **P99 Response Time**: {result['p99_response_time']:.3f}s
- **Avg CPU**: {result.get('avg_cpu_percent', 0):.1f}%
- **Avg Memory**: {result.get('avg_memory_mb', 0):.1f}MB (max {result.get('max_memory_mb', 0):.1f}MB)
"""
        
        report += f"""
## Analysis

### Performance Trends
- **FastAPI**: {'Shows async advantages at higher concurrency' if any(r['error_rate'] < 10 for r in fastapi_results) else 'Struggles with high concurrency'}
- **Django**: {'Maintains consistent performance' if any(r['error_rate'] < 10 for r in django_results) else 'Shows degradation at high concurrency'}

### Breaking Points
- **FastAPI Breaking Point**: {max([r['concurrent_users'] for r in fastapi_results if r['error_rate'] < 10], default='Unknown')} users
- **Django Breaking Point**: {max([r['concurrent_users'] for r in django_results if r['error_rate'] < 10], default='Unknown')} users

### Recommendations
- **For Low-Medium Concurrency**: Both frameworks perform well
- **For High Concurrency**: {'FastAPI' if max([r['throughput'] for r in fastapi_results if r['error_rate'] < 10], default=0) > max([r['throughput'] for r in django_results if r['error_rate'] < 10], default=0) else 'Django'} shows better performance
- **For Reliability**: {'Django' if any(r['error_rate'] == 0 for r in django_results) else 'FastAPI'} shows better error handling

---
*Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Report saved to {filename}")

async def main():
    parser = argparse.ArgumentParser(description='Simple Incremental FastAPI vs Django Benchmark')
    parser.add_argument('--fastapi-url', default='http://localhost:8000', help='FastAPI URL')
    parser.add_argument('--django-url', default='http://localhost:8001', help='Django URL')
    parser.add_argument('--max-concurrent', type=int, default=1000, help='Maximum concurrent users')
    parser.add_argument('--step', type=int, default=50, help='Step size for concurrency')
    parser.add_argument('--duration', type=int, default=30, help='Duration per test in seconds')
    
    args = parser.parse_args()
    
    benchmark = SimpleIncrementalBenchmark(args.fastapi_url, args.django_url)
    
    try:
        await benchmark.run_incremental_benchmark(
            max_concurrent=args.max_concurrent,
            step=args.step,
            duration=args.duration
        )
        
        benchmark.save_results()
        benchmark.generate_report()
        
        print("\n" + "="*80)
        print("INCREMENTAL BENCHMARK COMPLETED")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
        benchmark.save_results()
        benchmark.generate_report()

if __name__ == "__main__":
    asyncio.run(main())
