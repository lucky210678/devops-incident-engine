# guardrails/output_guard.py
import re

# High-risk destructive commands that must never be executed automatically
DESTRUCTIVE_COMMAND_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"kubectl\s+delete\s+(ns|namespace|node|all)",
    r"drop\s+database",
    r"truncate\s+table",
    r":\(\)\{\s*:\|:&\s*\};:",  # Fork bomb
    r"chmod\s+-R\s+777\s+/"
]

def sanitize_output(llm_response: str) -> dict:
    """
    Inspects generated LLM output for destructive actions before execution.
    """
    response_lower = llm_response.lower()
    
    for pattern in DESTRUCTIVE_COMMAND_PATTERNS:
        if re.search(pattern, response_lower):
            return {
                "is_safe": False,
                "sanitized_response": "[BLOCKED] Output contained prohibited destructive commands.",
                "blocked_pattern": pattern
            }
            
    return {
        "is_safe": True,
        "sanitized_response": llm_response,
        "blocked_pattern": None
    }