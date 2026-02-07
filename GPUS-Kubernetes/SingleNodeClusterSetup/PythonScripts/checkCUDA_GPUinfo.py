"""
CUDA and GPU Availability Checker

A simple diagnostic script to verify CUDA/GPU setup for PyTorch workloads.
Run this script to quickly check if your GPU is properly configured and
accessible to PyTorch before running more complex GPU workloads.

Output includes:
- CUDA availability status
- GPU device name (e.g., "NVIDIA GeForce RTX 4090")
- Total number of available GPUs

Usage:
    python checkCUDA_GPUinfo.py
"""

import torch

# Check if CUDA (NVIDIA GPU support) is available in this PyTorch installation
# This verifies both driver installation and PyTorch CUDA bindings
if torch.cuda.is_available():
    print("CUDA is available")

    # Get the name of the first GPU (index 0)
    # Useful for identifying the GPU model and confirming correct device detection
    print("GPU Name:", torch.cuda.get_device_name(0))

    # Count total number of GPUs accessible to PyTorch
    # Important for multi-GPU training configurations
    print("Number of GPUs:", torch.cuda.device_count())

else:
    # CUDA not available - could be due to:
    # - No NVIDIA GPU present
    # - NVIDIA drivers not installed
    # - PyTorch installed without CUDA support (CPU-only build)
    print("CUDA is not available")
