#!/bin/bash
# =============================================================================
# PyTorch Distributed Training Launcher Script
# =============================================================================
#
# This script launches distributed PyTorch training across multiple nodes
# using torchrun (the recommended replacement for torch.distributed.launch).
#
# Required Environment Variables:
#   NUM_TRAINERS  - Number of GPU processes per node (typically = number of GPUs)
#   NUM_NODES     - Total number of nodes participating in training
#   NODE_RANK     - This node's rank (0 for master, 1+ for workers)
#   MASTER_ADDR   - IP address or hostname of the master node (rank 0)
#   MASTER_PORT   - Port for distributed communication (e.g., 29500)
#
# Example usage for 2-node training with 4 GPUs each:
#   On master (node 0):
#     NUM_TRAINERS=4 NUM_NODES=2 NODE_RANK=0 MASTER_ADDR=192.168.1.100 MASTER_PORT=29500 ./launcher.sh
#   On worker (node 1):
#     NUM_TRAINERS=4 NUM_NODES=2 NODE_RANK=1 MASTER_ADDR=192.168.1.100 MASTER_PORT=29500 ./launcher.sh
# =============================================================================

# Set NCCL debug level to WARN to reduce log verbosity
# Options: TRACE, INFO, WARN (default shows only warnings and errors)
# Set to INFO or TRACE for debugging communication issues
export NCCL_DEBUG=WARN

# Launch distributed training using torchrun
# torchrun handles process spawning, environment setup, and fault tolerance
torchrun \
    --nproc_per_node=$NUM_TRAINERS \
    --nnodes=$NUM_NODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --master_port=$MASTER_PORT \
    ./main.py

# Parameter explanations:
# --nproc_per_node: Number of processes (GPUs) to spawn on this node
# --nnodes: Total number of nodes in the distributed training cluster
# --node_rank: Unique identifier for this node (0 = master, 1+ = workers)
# --master_addr: Network address of the rank 0 node for coordination
# --master_port: TCP port for the distributed communication rendezvous
