"""
FastAPI LLM Inference Service

A REST API service for running inference on HuggingFace language models.
This containerized application provides a simple HTTP endpoint for text
generation using GPU-accelerated transformer models.

Endpoints:
    POST /predict - Generate text based on input prompt

Features:
    - GPU-accelerated inference when CUDA is available
    - Configurable max token generation length
    - Nucleus sampling (top-p) with top-k filtering for diverse outputs

Dependencies:
    - FastAPI for the REST API framework
    - PyTorch for tensor operations and GPU support
    - model_loader.py for HuggingFace model initialization
"""

from fastapi import FastAPI
from pydantic import BaseModel
import torch
from model_loader import load_model

# Load the model and tokenizer at startup
# This happens once when the container starts, not per-request
# The model is loaded based on the MODEL_PATH environment variable
tokenizer, model = load_model()

# Initialize FastAPI application
app = FastAPI()


class Prompt(BaseModel):
    """
    Request schema for the /predict endpoint.

    Attributes:
        text: The input prompt text to generate a response for
        max_tokens: Maximum number of new tokens to generate (default: 50)
    """
    text: str
    max_tokens: int = 50


@app.post("/predict")
def predict(prompt: Prompt):
    """
    Generate text based on the input prompt.

    This endpoint tokenizes the input, runs inference on the model,
    and returns the generated text. Uses nucleus sampling for
    more natural and diverse text generation.

    Args:
        prompt: Prompt object containing text and max_tokens

    Returns:
        dict: {"output": "generated text..."}
    """
    # Determine which device the model is on (CPU or CUDA)
    # This ensures input tensors are placed on the same device as the model
    device = next(iter(model.parameters())).device

    # Tokenize the input text and move tensors to the model's device
    inputs = tokenizer(prompt.text, return_tensors="pt").to(device)

    # Run inference without gradient computation for efficiency
    # Gradients are only needed during training, not inference
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=prompt.max_tokens,  # Limit output length
            do_sample=True,   # Enable sampling (vs greedy decoding)
            top_k=50,         # Consider only top 50 tokens at each step
            top_p=0.95        # Nucleus sampling: use tokens comprising 95% probability mass
        )

    # Decode the output token IDs back to text
    # skip_special_tokens=True removes tokens like <pad>, <eos>, etc.
    return {"output": tokenizer.decode(outputs[0], skip_special_tokens=True)}
