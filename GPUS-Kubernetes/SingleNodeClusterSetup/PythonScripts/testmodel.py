"""
LLaMA Model Inference Test Script

This script demonstrates loading and running inference on a LLaMA-3B model
using HuggingFace Transformers with automatic mixed precision selection.

The script automatically selects the best precision mode for your hardware:
- BF16 (bfloat16) on Ada/Hopper GPUs (RTX 40xx, A100, H100)
- FP16 (float16) on older GPUs (RTX 30xx, V100)
- FP32 (float32) on CPU

Features:
- Automatic device placement with device_map="auto"
- Chat template formatting for instruction-tuned models
- HuggingFace pipeline for simplified inference

Prerequisites:
- Model files downloaded to MODEL_DIR path
- NVIDIA GPU with sufficient VRAM (~6GB for 3B model in half precision)
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Path to local model directory - update this to match your setup
# Can be a local path or a HuggingFace Hub model ID
MODEL_DIR = "/root/GPU-VastAI/K8s/SingleNodeClusterSetup/models/meta-llama-3B"

# Automatic precision selection based on GPU capabilities
# - BF16: Better numerical range, preferred on modern GPUs (Ada Lovelace, Hopper)
# - FP16: Wider compatibility, works on Ampere and older architectures
# - FP32: Full precision fallback for CPU
if torch.cuda.is_available():
    # Check if GPU supports bfloat16 natively (Ada/Hopper architectures)
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    # "auto" device_map distributes model across available GPUs automatically
    device_map = "auto"
else:
    # CPU fallback: use full precision (FP32)
    dtype = torch.float32
    device_map = None

print(f"Loading model from: {MODEL_DIR}")

# Load tokenizer with fast (Rust-based) implementation for speed
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=True)

# Load model with automatic layer placement and memory optimization
model = AutoModelForCausalLM.from_pretrained(
    MODEL_DIR,
    torch_dtype=dtype,           # Use selected precision (bf16/fp16/fp32)
    device_map=device_map,       # Automatically place layers on GPU(s)
    low_cpu_mem_usage=True       # Load weights incrementally to reduce RAM usage
    # Optional: Enable FlashAttention for faster inference on supported GPUs:
    # attn_implementation="flash_attention_2",
)

# Build a chat-style prompt using the model's built-in chat template
# This formats the conversation correctly for instruction-tuned models
messages = [
    # System message sets the model's behavior/persona
    {"role": "system", "content": "You are a helpful assistant."},
    # User message contains the actual query
    {
        "role": "user",
        "content": "In one paragraph, explain VRAM usage for LLMs (weights, activations, KV cache) in simple terms."
    },
]

# Convert messages to the model's expected prompt format
# add_generation_prompt=True adds the assistant's turn marker at the end
prompt = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,  # Add assistant turn marker for generation
    tokenize=False               # Return string, not token IDs
)

# Create a text-generation pipeline for simplified inference
# Pipeline handles tokenization, generation, and decoding automatically
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=dtype,
    device_map=device_map
)

# Generation hyperparameters - adjust these to control output quality
GEN_KW = dict(
    max_new_tokens=256,          # Maximum tokens to generate
    temperature=0.7,             # Higher = more creative, lower = more focused
    top_p=0.9,                   # Nucleus sampling: consider top 90% probability mass
    do_sample=True,              # Enable sampling (vs greedy decoding)
    repetition_penalty=1.1,      # Penalize repeating tokens (reduces loops)
    eos_token_id=tokenizer.eos_token_id,  # Stop at end-of-sequence token
)

print("\n=== Model Response ===\n")

# Run generation and get the output text
out = pipe(prompt, **GEN_KW)[0]["generated_text"]

# The pipeline returns prompt + completion concatenated
# Slice off the prompt to show only the model's response
print(out[len(prompt):].strip())
