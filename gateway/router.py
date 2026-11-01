# gateway/router.py

# gateway/router.py

def route_task(task_description: str) -> str:
    """
    Smart Router Logic:
    Analyzes task complexity and dynamically assigns the optimal model target.
    """
    task_lower = task_description.lower()
    
    # Complex diagnostic keywords requiring high-capability reasoning
    complex_keywords = [
        "root cause", "crashloop", "deadlock", 
        "oomkilled", "security", "heap dump", "critical"
    ]
    
    if any(keyword in task_lower for keyword in complex_keywords):
        return "groq/llama-3.3-70b-versatile"
    else:
        return "groq/llama-3.1-8b-instant"