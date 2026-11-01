# tools/kubectl_simulator.py

def get_pod_logs(pod_name: str) -> str:
    """
    Simulates fetching Kubernetes pod logs via kubectl.
    """
    return (
        f"[Kubectl Log Output for '{pod_name}']\n"
        f"2026-11-01T23:50:11Z ERROR java.lang.OutOfMemoryError: Java heap space\n"
        f"2026-11-01T23:50:12Z FATAL Container auth-service terminated with exit code 137 (OOMKilled).\n"
        f"Memory Limit: 256Mi | Memory Usage: 258Mi"
    )