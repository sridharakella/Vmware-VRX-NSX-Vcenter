"""
Bare Metal LLM Inference Script (FP32 Default Precision)

This script loads and runs HuggingFace language models directly on bare metal
(without containerization) using full FP32 precision. This is useful for:
- Baseline performance comparisons against half-precision modes
- Maximum numerical accuracy when precision matters
- Models that don't support half-precision

The script supports any HuggingFace model that uses the AutoModelForCausalLM
architecture (GPT-2, LLaMA, Qwen, Mistral, etc.).

Environment Variables:
    MODEL_PATH: HuggingFace model ID or local path (default: "gpt2")
    TRUST_REMOTE_CODE: Set to "1" or "true" for models with custom code
    MAX_NEW_TOKENS: Maximum tokens to generate (default: 200)
    PYTORCH_CUDA_ALLOC_CONF: CUDA memory allocator configuration

Usage:
    export MODEL_PATH="Qwen/Qwen2.5-3B-Instruct"
    python run_model_default.py
"""

import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model(model_name_or_path=None):
    """
    Load a HuggingFace model and tokenizer in FP32 precision.

    This function loads the model in full 32-bit floating point precision,
    which uses more VRAM but provides maximum numerical accuracy.

    Args:
        model_name_or_path: HuggingFace model ID or local path.
                           Falls back to MODEL_PATH env var or "gpt2".

    Returns:
        tuple: (tokenizer, model, device) - The loaded components and device string
    """
    # Use provided path, environment variable, or default to gpt2
    model_name_or_path = model_name_or_path or os.getenv("MODEL_PATH", "gpt2")

    # Check if we should trust custom model code (required for some models like Qwen)
    trust_remote = os.getenv("TRUST_REMOTE_CODE", "0") in ("1", "true", "True")

    print(f"Loading model from: {model_name_or_path}")

    # Start timing the model load
    start = time.time()

    # Load the tokenizer for text encoding/decoding
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=trust_remote)

    # Load the model in FP32 (no dtype specified = default precision)
    # low_cpu_mem_usage=True loads weights sequentially to reduce peak RAM usage
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        low_cpu_mem_usage=True,  # Load weights incrementally to save RAM
        trust_remote_code=trust_remote,
        # No dtype specified -> FP32 by default (full precision)
    )

    # Select device: GPU if available, otherwise CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    load_time = time.time() - start

    print(f"Model loaded on {device.upper()} in {load_time:.2f} seconds")

    # Print GPU memory stats if using CUDA
    if device == "cuda":
        # Ensure all CUDA operations are complete before measuring memory
        torch.cuda.synchronize()
        print(f"GPU memory allocated: {torch.cuda.memory_allocated()/1e9:.2f} GB")
        print(f"GPU memory reserved : {torch.cuda.memory_reserved()/1e9:.2f} GB")

    return tokenizer, model, device


def generate_text(tokenizer, model, device, prompt, max_new_tokens=200):
    """
    Generate text from the model given an input prompt.

    Uses nucleus sampling (top-p) combined with top-k filtering for
    diverse but coherent text generation.

    Args:
        tokenizer: HuggingFace tokenizer for encoding/decoding
        model: The loaded language model
        device: Device string ("cuda" or "cpu")
        prompt: Input text to generate from
        max_new_tokens: Maximum number of tokens to generate
    """
    # Tokenize input and move tensors to the model's device
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    print(f"\nRunning inference (max_new_tokens={max_new_tokens})...")
    start = time.time()

    # Disable gradient computation for inference (saves memory and compute)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,   # Enable sampling for varied outputs
            top_k=50,         # Consider top 50 tokens at each step
            top_p=0.95,       # Nucleus sampling: use tokens in top 95% probability mass
            use_cache=True,   # Enable KV cache for faster autoregressive generation
        )

    elapsed = time.time() - start

    # Decode token IDs back to text, removing special tokens
    text_out = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Inference time: {elapsed:.2f}s\n")
    print("Output:")
    print(text_out)


if __name__ == "__main__":
    # Configure CUDA memory allocator to reduce fragmentation
    # expandable_segments allows the allocator to grow dynamically
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    # Load configuration from environment variables
    model_name = os.getenv("MODEL_PATH", "gpt2")
    max_new = int(os.getenv("MAX_NEW_TOKENS", "200"))

    # Get prompt from user input
    prompt = input("Enter your prompt: ")

    # Load model and run generation
    tokenizer, model, device = load_model(model_name)
    generate_text(tokenizer, model, device, prompt, max_new_tokens=max_new)
