# guardrails/input_guard.py
import re

# Common prompt injection triggers
INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"system override",
    r"you are now a",
    r"disregard safety filters",
    r"drop all tables"
]

# Regex patterns for sensitive data masking
PII_PATTERNS = {
    "api_key": r"(sk-[a-zA-Z0-9]{32,}|gsk_[a-zA-Z0-9]{32,})",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
}

def check_prompt_injection(prompt: str) -> bool:
    """Returns True if a prompt injection attempt is detected."""
    prompt_lower = prompt.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True
    return False

def sanitize_input(prompt: str) -> dict:
    """
    Validates input safety and redacts sensitive information.
    """
    if check_prompt_injection(prompt):
        return {
            "is_safe": False,
            "sanitized_prompt": "",
            "reason": "Security Alert: Prompt injection attempt detected."
        }
    
    sanitized = prompt
    # Redact sensitive data
    for key, pattern in PII_PATTERNS.items():
        sanitized = re.sub(pattern, f"[{key.upper()}_REDACTED]", sanitized)
        
    return {
        "is_safe": True,
        "sanitized_prompt": sanitized,
        "reason": "Passed input safety checks."
    }