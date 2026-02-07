#!/bin/bash
# =============================================================================
# Kubernetes GPU Cluster Full Setup Script
# =============================================================================
#
# This is the main orchestration script that sets up a complete single-node
# Kubernetes cluster with GPU support and monitoring capabilities.
#
# Execution order:
#   1. preChecks.sh    - Verify system prerequisites (Docker, kubeadm, etc.)
#   2. controlNode.sh  - Initialize Kubernetes control plane
#   3. GPUNodes.sh     - Install NVIDIA GPU Operator for GPU access
#   4. monitoring.sh   - Deploy Prometheus/Grafana monitoring stack
#   5. Apply GPU ServiceMonitor for DCGM metrics collection
#
# Prerequisites:
#   - Ubuntu/Debian-based system with NVIDIA GPU
#   - NVIDIA drivers installed
#   - Root/sudo access
#   - All component scripts in the same directory
#
# Usage:
#   chmod +x runall.sh && ./runall.sh
# =============================================================================

# Exit immediately on any error, treat unset variables as errors,
# and fail on any command in a pipeline that fails
set -euo pipefail

# Resolve this script's directory to allow running from any location
# This ensures all relative paths work correctly regardless of where
# the script is invoked from
DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# Define the core scripts that must be present for the setup to work
# These scripts are executed in order and each must complete successfully
CORE_SCRIPTS=(
  "preChecks.sh"      # System prerequisites validation
  "controlNode.sh"    # Kubernetes control plane initialization
  "GPUNodes.sh"       # NVIDIA GPU Operator installation
  "monitoring.sh"     # Prometheus/Grafana stack deployment
)

# Verify all core scripts exist and make them executable
# This prevents runtime failures due to missing dependencies
for s in "${CORE_SCRIPTS[@]}"; do
  if [[ ! -f "$DIR/$s" ]]; then
    echo "Missing: $s (expected in $DIR)"
    exit 1
  fi
  chmod +x "$DIR/$s"
done

# Execute each setup phase in sequence
echo "Running prechecks..."
"$DIR/preChecks.sh"

echo "Setting up control plane..."
"$DIR/controlNode.sh"

echo "Setting up GPU node(s)..."
"$DIR/GPUNodes.sh"

echo "Installing monitoring stack (Prometheus/Grafana) and starting port-forward (if any)..."
"$DIR/monitoring.sh"


# Print helpful connection instructions for accessing Grafana remotely
# Users need to set up SSH port forwarding to access the Grafana dashboard
echo
echo "From your laptop, open an SSH tunnel to Grafana then browse:"
echo "    ssh -p <SSH_PORT> -N -L 3000:localhost:80 <user>@<public_ip>"
echo "    -> http://localhost:3000"

# Apply the ServiceMonitor for DCGM (Data Center GPU Manager) exporter
# This enables Prometheus to scrape GPU metrics like utilization,
# temperature, memory usage, and power consumption
kubectl apply -f "$DIR/serviceMonitorGPU.yml"
