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

# Sort by concurrency
fas.sort(key=lambda r: r['concurrent_users'])
djs.sort(key=lambda r: r['concurrent_users'])

x_f = [r['concurrent_users'] for r in fas]
x_d = [r['concurrent_users'] for r in djs]

# Throughput plot
plt.figure(figsize=(8,5))
plt.plot(x_f, [r['throughput'] for r in fas], marker='o', label='FastAPI')
plt.plot(x_d, [r['throughput'] for r in djs], marker='o', label='Django')
plt.title('Throughput vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Throughput (RPS)')
plt.grid(True, alpha=0.3)
plt.legend()
throughput_png = OUT_DIR / 'throughput_vs_concurrency.png'
plt.savefig(throughput_png, bbox_inches='tight')
plt.close()

# Error rate plot
plt.figure(figsize=(8,5))
plt.plot(x_f, [r['error_rate'] for r in fas], marker='o', label='FastAPI')
plt.plot(x_d, [r['error_rate'] for r in djs], marker='o', label='Django')
plt.title('Error Rate vs Concurrency')
plt.xlabel('Concurrent Users')
plt.ylabel('Error Rate (%)')
plt.grid(True, alpha=0.3)
plt.legend()
errors_png = OUT_DIR / 'error_rate_vs_concurrency.png'
plt.savefig(errors_png, bbox_inches='tight')
plt.close()

print(f'Wrote {throughput_png} and {errors_png}')
