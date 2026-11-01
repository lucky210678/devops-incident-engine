# tools/db_diagnostics.py

def get_db_metrics(db_instance: str) -> str:
    """
    Simulates fetching database performance metrics.
    """
    return (
        f"[Database Health Metrics for '{db_instance}']\n"
        f"Status: DEGRADED\n"
        f"Active Connections: 498/500 (99.6% Capacity)\n"
        f"Query Queue Depth: 142 waiting queries\n"
        f"Primary Bottleneck: Connection pool exhaustion"
    )