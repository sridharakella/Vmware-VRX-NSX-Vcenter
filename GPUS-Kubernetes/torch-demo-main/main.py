"""
PyTorch Distributed Training Template

This script provides a minimal template for distributed training across
multiple GPUs and/or multiple nodes using PyTorch's distributed package.

Key Concepts:
- World Size: Total number of processes across all nodes
- Global Rank: Unique identifier for each process (0 to world_size-1)
- Local Rank: Process index within a single node (0 to num_gpus_per_node-1)
- NCCL Backend: NVIDIA Collective Communications Library for GPU-to-GPU communication

This template is designed to be launched with torchrun (see launcher.sh):
    torchrun --nproc_per_node=4 --nnodes=2 --node_rank=0 \\
             --master_addr=192.168.1.100 --master_port=29500 main.py

Environment Variables (set by torchrun):
    LOCAL_RANK: This process's GPU index on the local node
    RANK: This process's global rank across all nodes
    WORLD_SIZE: Total number of processes
    MASTER_ADDR: Address of the rank 0 process
    MASTER_PORT: Port for distributed communication
"""

import os
import torch
import torch.distributed as dist


def init_distributed():
    """
    Initialize the distributed training environment.

    This function sets up the process group for distributed training using
    the NCCL backend (optimized for NVIDIA GPUs). It reads environment
    variables set by torchrun to configure the distributed setup.

    Returns:
        tuple: (local_rank, global_rank, world_size, device)
            - local_rank: GPU index on this node (0 to num_gpus-1)
            - global_rank: Unique process ID across all nodes
            - world_size: Total number of processes
            - device: torch.device for this process's GPU
    """
    # Initialize the process group with NCCL backend
    # NCCL (NVIDIA Collective Communications Library) is the fastest
    # backend for GPU-to-GPU communication on NVIDIA hardware
    dist.init_process_group(backend="nccl")

    # LOCAL_RANK: Which GPU on THIS node (set by torchrun)
    # Used to assign each process to a specific GPU
    local_rank = int(os.environ["LOCAL_RANK"])

    # Global rank: Unique ID across ALL nodes (0 to world_size-1)
    # Rank 0 is typically the "master" that coordinates operations
    global_rank = dist.get_rank()

    # World size: Total number of processes across all nodes
    # For 2 nodes with 4 GPUs each: world_size = 8
    world_size = dist.get_world_size()

    # Create device handle for this process's GPU
    # Each process gets exactly one GPU based on its local rank
    device = torch.device(f"cuda:{local_rank}")

    # Set the default CUDA device for this process
    # All subsequent CUDA operations will use this GPU
    torch.cuda.set_device(device)

    return local_rank, global_rank, world_size, device


def cleanup_distributed():
    """
    Clean up the distributed environment.

    This function should be called at the end of training to properly
    shut down the process group and release resources. Failing to call
    this may result in hanging processes or resource leaks.
    """
    dist.destroy_process_group()


def main():
    """
    Main entry point for distributed training.

    This is a template - add your training code in the marked section.
    The distributed environment is automatically initialized and cleaned up.
    """
    # Initialize distributed environment and get process info
    local_rank, global_rank, world_size, device = init_distributed()

    # Log process information (useful for debugging multi-node setups)
    print(f"Running on rank {global_rank}/{world_size-1} (local rank: {local_rank}), device: {device}")

    # ================================================================
    # YOUR TRAINING CODE HERE
    # ================================================================
    # Example operations you might add:
    # - Create model and wrap with DistributedDataParallel (DDP)
    # - Create DistributedSampler for your DataLoader
    # - Training loop with gradient synchronization
    # - Save checkpoints (typically only on rank 0)
    # ================================================================

    # Clean up distributed environment when done
    # This ensures proper shutdown of all processes
    cleanup_distributed()


if __name__ == "__main__":
    main()
