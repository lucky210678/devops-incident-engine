# gateway/client.py
import os
import litellm
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Active provider models to try in sequence
DEFAULT_FALLBACK_MODELS = [
    "groq/llama-3.1-70b-versatile",
    "groq/llama-3.2-3b-preview",
    "groq/deepseek-r1-distill-llama-70b"
]

def mock_fallback_llm(prompt: str) -> str:
    """Offline mock LLM engine used when cloud providers are unreachable or deprecated."""
    prompt_lower = prompt.lower()
    if "greeting" in prompt_lower or "hello" in prompt_lower:
        return "[Mock LLM Response] Welcome to the DevOps Incident Response Copilot! System monitoring is active."
    elif "k8s" in prompt_lower or "pod" in prompt_lower:
        return "[Mock LLM Response] Analyzing Kubernetes logs: Pod failure detected due to resource exhaustion."
    elif "db" in prompt_lower or "database" in prompt_lower:
        return "[Mock LLM Response] Analyzing Database health: High active connection count causing latency."
    return f"[Mock LLM Response] Successfully processed prompt: '{prompt[:50]}...'"

def call_llm(prompt: str, model_name: str = "groq/llama-3.1-70b-versatile", temperature: float = 0.2) -> str:
    """
    Unified LLM gateway call with automatic cloud fallbacks and local mock fallback.
    """
    models_to_try = [model_name] + [m for m in DEFAULT_FALLBACK_MODELS if m != model_name]
    
    for model in models_to_try:
        try:
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[Gateway Notice] Model '{model}' failed. Reason: {e}")
            print("Attempting fallback to next model...\n")
            continue

    # Final resilient fallback if all API calls fail
    print("[Gateway Notice] All cloud LLM endpoints failed. Triggering local mock fallback engine...")
    return mock_fallback_llm(prompt)