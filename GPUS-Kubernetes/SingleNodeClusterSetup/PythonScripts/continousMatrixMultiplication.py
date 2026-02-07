"""
Continuous GPU Matrix Multiplication Stress Test

This script performs continuous matrix multiplication on the GPU to stress-test
CUDA performance and GPU stability. It creates two large random matrices and
repeatedly multiplies them, reporting iteration count and elapsed time.

Use cases:
- GPU burn-in testing to verify hardware stability
- Monitoring GPU temperature and power consumption under sustained load
- Benchmarking sustained GPU compute throughput

The 15000x15000 matrix size is chosen to fully utilize GPU memory and compute
units on most modern GPUs (requires ~1.7GB VRAM per matrix in FP32).
"""

import torch
import time

# Create two large random matrices directly on the GPU
# Shape: 15000x15000 = 225 million elements per matrix
# Memory: ~900MB per matrix in FP32 (4 bytes per element)
x = torch.rand(15000, 15000).cuda()
y = torch.rand(15000, 15000).cuda()

# Initialize iteration counter and start timer for performance tracking
iters = 0
start = time.time()

# Infinite loop for continuous GPU stress testing
# Press Ctrl+C to stop the script
while True:
    # Perform matrix multiplication on GPU
    # This is a compute-intensive operation that fully utilizes GPU cores
    # Result z is a 15000x15000 matrix (not stored, just computed)
    z = torch.matmul(x, y)

    # Increment iteration counter
    iters += 1

    # Calculate total elapsed time since start
    elapsed = time.time() - start

    # Print progress every 10 iterations to avoid console spam
    # while still providing regular performance feedback
    if iters % 10 == 0:
        print(f"Iters: {iters}, Elapsed: {elapsed:.2f}s")
