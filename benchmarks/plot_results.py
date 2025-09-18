#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS_JSON = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('results/incremental_benchmark_results.json')
OUT_DIR = RESULTS_JSON.parent

with open(RESULTS_JSON) as f:
    data = json.load(f)

# Group by framework
fas = [r for r in data if r['framework'] == 'fastapi']
djs = [r for r in data if r['framework'] == 'django']
djs_asgi = [r for r in data if r['framework'] == 'django-asgi']

# Sort by concurrency
fas.sort(key=lambda r: r['concurrent_users'])
djs.sort(key=lambda r: r['concurrent_users'])
djs_asgi.sort(key=lambda r: r['concurrent_users'])

x_f = [r['concurrent_users'] for r in fas]
x_d = [r['concurrent_users'] for r in djs]
x_d_asgi = [r['concurrent_users'] for r in djs_asgi]

# Throughput plot
plt.figure(figsize=(10,6))
plt.plot(x_f, [r['throughput'] for r in fas], marker='o', label='FastAPI', linewidth=2)
plt.plot(x_d, [r['throughput'] for r in djs], marker='s', label='Django WSGI', linewidth=2)
plt.plot(x_d_asgi, [r['throughput'] for r in djs_asgi], marker='^', label='Django ASGI', linewidth=2)
plt.title('Throughput vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Throughput (RPS)')
plt.grid(True, alpha=0.3)
plt.legend()
throughput_png = OUT_DIR / 'throughput_vs_concurrency.png'
plt.savefig(throughput_png, bbox_inches='tight')
plt.close()

# Error rate plot
plt.figure(figsize=(10,6))
plt.plot(x_f, [r['error_rate'] for r in fas], marker='o', label='FastAPI', linewidth=2)
plt.plot(x_d, [r['error_rate'] for r in djs], marker='s', label='Django WSGI', linewidth=2)
plt.plot(x_d_asgi, [r['error_rate'] for r in djs_asgi], marker='^', label='Django ASGI', linewidth=2)
plt.title('Error Rate vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Error Rate (%)')
plt.grid(True, alpha=0.3)
plt.legend()
errors_png = OUT_DIR / 'error_rate_vs_concurrency.png'
plt.savefig(errors_png, bbox_inches='tight')
plt.close()

# CPU usage plot
plt.figure(figsize=(10,6))
plt.plot(x_f, [r['avg_cpu_percent'] for r in fas], marker='o', label='FastAPI', linewidth=2)
plt.plot(x_d, [r['avg_cpu_percent'] for r in djs], marker='s', label='Django WSGI', linewidth=2)
plt.plot(x_d_asgi, [r['avg_cpu_percent'] for r in djs_asgi], marker='^', label='Django ASGI', linewidth=2)
plt.title('CPU Usage vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Average CPU Usage (%)')
plt.grid(True, alpha=0.3)
plt.legend()
cpu_png = OUT_DIR / 'cpu_usage_vs_concurrency.png'
plt.savefig(cpu_png, bbox_inches='tight')
plt.close()

# Duration plot
plt.figure(figsize=(10,6))
plt.plot(x_f, [r['duration'] for r in fas], marker='o', label='FastAPI', linewidth=2)
plt.plot(x_d, [r['duration'] for r in djs], marker='s', label='Django WSGI', linewidth=2)
plt.plot(x_d_asgi, [r['duration'] for r in djs_asgi], marker='^', label='Django ASGI', linewidth=2)
plt.title('Test Duration vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Duration (seconds)')
plt.grid(True, alpha=0.3)
plt.legend()
duration_png = OUT_DIR / 'duration_vs_concurrency.png'
plt.savefig(duration_png, bbox_inches='tight')
plt.close()

# Total requests plot
plt.figure(figsize=(10,6))
plt.plot(x_f, [r['total_requests'] for r in fas], marker='o', label='FastAPI', linewidth=2)
plt.plot(x_d, [r['total_requests'] for r in djs], marker='s', label='Django WSGI', linewidth=2)
plt.plot(x_d_asgi, [r['total_requests'] for r in djs_asgi], marker='^', label='Django ASGI', linewidth=2)
plt.title('Total Requests vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Total Requests')
plt.grid(True, alpha=0.3)
plt.legend()
requests_png = OUT_DIR / 'total_requests_vs_concurrency.png'
plt.savefig(requests_png, bbox_inches='tight')
plt.close()

print(f'Wrote {throughput_png}, {errors_png}, {cpu_png}, {duration_png}, and {requests_png}')
