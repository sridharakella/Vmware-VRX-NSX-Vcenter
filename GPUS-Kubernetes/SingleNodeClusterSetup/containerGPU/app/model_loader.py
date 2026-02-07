"""
HuggingFace Model Loader for Containerized GPU Inference

This module handles loading large language models (LLMs) from HuggingFace Hub
or local paths for use in a containerized FastAPI application.

Key features:
- Supports both HuggingFace Hub model IDs (e.g., 'Qwen/Qwen2.5-3B-Instruct')
  and local filesystem paths
- Automatic GPU detection with CPU fallback
- FP16 precision for reduced VRAM usage on GPU
- trust_remote_code=True for models with custom implementations

Environment Variables:
    MODEL_PATH: Required. HuggingFace model ID or local path to model files.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model():
    """
    Load a HuggingFace causal language model and its tokenizer.

    This function reads the MODEL_PATH environment variable to determine
    which model to load. It automatically configures the model for optimal
    performance based on available hardware (GPU vs CPU).

    Returns:
        tuple: (tokenizer, model) - The loaded tokenizer and model objects

    Raises:
        RuntimeError: If MODEL_PATH environment variable is not set

    Notes:
        - Uses FP16 precision on GPU to reduce VRAM usage by ~50%
        - trust_remote_code=True allows loading models with custom code
          (required for models like Qwen that have custom implementations)
        - use_fast=True uses the faster Rust-based tokenizer when available
    """
    # Get model path from environment variable
    # This allows configuration via Kubernetes ConfigMaps or Docker env vars
    model_id = os.getenv("MODEL_PATH")
    if not model_id:
        raise RuntimeError("MODEL_PATH not set (HF repo id like 'Qwen/Qwen2.5-3B-Instruct' or a local path).")

    print(f"Loading model from: {model_id}")

    # Load tokenizer with fast implementation for better performance
    # trust_remote_code=True is required for models with custom tokenizer code
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True, trust_remote_code=True)

    # Load the model with appropriate precision settings
    # - FP16 on GPU: Reduces VRAM usage from ~12GB to ~6GB for 3B param models
    # - FP32 on CPU: Full precision when CUDA is not available
    # trust_remote_code=True allows models with custom architectures (e.g., Qwen)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else None,
    )

    # Move model to GPU if CUDA is available
    # This is done after loading to allow for potential memory optimizations
    if torch.cuda.is_available():
        model = model.to("cuda")
        print("Model loaded on GPU")
    else:
        print("CUDA not available, running on CPU")

    return tokenizer, model
