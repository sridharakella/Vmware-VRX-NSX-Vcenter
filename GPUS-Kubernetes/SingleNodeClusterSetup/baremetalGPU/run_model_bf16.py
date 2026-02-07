"""
Bare Metal LLM Inference Script (BF16/FP16 Half Precision)

This script loads and runs HuggingFace language models directly on bare metal
using half precision (BF16 or FP16) to minimize VRAM usage while maintaining
good inference quality.

Half precision benefits:
- ~50% reduction in VRAM usage compared to FP32
- Faster inference on modern GPUs with tensor cores
- BF16 preferred on Ada/Hopper (RTX 40xx, A100, H100) for better numerical range
- FP16 fallback for older architectures (Ampere, Turing, Volta)

The script supports any HuggingFace model that uses the AutoModelForCausalLM
architecture (GPT-2, LLaMA, Qwen, Mistral, etc.).

Environment Variables:
    MODEL_PATH: HuggingFace model ID or local path (default: "gpt2")
    TRUST_REMOTE_CODE: Set to "1" or "true" for models with custom code
    MAX_NEW_TOKENS: Maximum tokens to generate (default: 200)
    PYTORCH_CUDA_ALLOC_CONF: CUDA memory allocator configuration

Usage:
    export MODEL_PATH="Qwen/Qwen2.5-3B-Instruct"
    python run_model_bf16.py
"""

import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def pick_half_precision_dtype():
    """
    Select the optimal half-precision dtype for the current GPU.

    BF16 (bfloat16) is preferred on modern GPUs (Ada Lovelace, Hopper)
    because it has better numerical range than FP16, reducing overflow issues.
    Falls back to FP16 for older GPU architectures.

    Returns:
        torch.dtype: Either torch.bfloat16 or torch.float16
    """
    if torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        return torch.bfloat16
    return torch.float16


def load_model(model_name_or_path=None):
    """
    Load a HuggingFace model and tokenizer in half precision.

    This function loads the model in BF16 or FP16 precision to reduce
    VRAM usage by approximately 50% compared to FP32, enabling larger
    models to fit in memory.

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

    # Select optimal half-precision dtype for this GPU
    dtype = pick_half_precision_dtype()
    print(f"Using dtype: {dtype}")

    # Start timing the model load
    start = time.time()

    # Load the tokenizer for text encoding/decoding
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=trust_remote)

    # Load the model in half precision to reduce VRAM usage
    # Note: Using 'dtype' parameter instead of 'torch_dtype' (model-specific)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        dtype=dtype,              # Half precision (bf16 or fp16)
        low_cpu_mem_usage=True,   # Load weights incrementally to save RAM
        trust_remote_code=trust_remote,
    )
    load_time = time.time() - start

    # Select device: GPU if available, otherwise CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

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
    diverse but coherent text generation. KV cache is enabled for
    faster autoregressive generation.

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
    # Load configuration from environment variables
    # MODEL_PATH: e.g. export MODEL_PATH="Qwen/Qwen3-4B-Instruct-2507"
    # MAX_NEW_TOKENS: e.g. export MAX_NEW_TOKENS=120
    model_name = os.getenv("MODEL_PATH", "gpt2")
    max_new = int(os.getenv("MAX_NEW_TOKENS", "200"))

    # Configure CUDA memory allocator to reduce fragmentation
    # expandable_segments allows the allocator to grow dynamically
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    # Get prompt from user input
    prompt = input("Enter your prompt: ")

    # Load model and run generation
    tokenizer, model, device = load_model(model_name)
    generate_text(tokenizer, model, device, prompt, max_new_tokens=max_new)
