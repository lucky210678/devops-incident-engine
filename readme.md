# 🚨 Enterprise DevOps Incident Response Copilot

An autonomous, multi-agent AI copilot designed to triage production infrastructure alerts, run diagnostic tooling, apply security guardrails, and execute remediation workflows with fail-safe LLM routing.

---

## 📐 System Architecture

```text
+-----------------------------------------------------------------------+
|                    DevOps Incident Response Copilot                   |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 1. Gateway & Router (`gateway/`)                                      |
|    - Task Complexity Analysis (Router)                                |
|    - LiteLLM Unified Client & Tiered Cloud/Local Fallback Engine      |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 2. Safety Layer (`guardrails/`)                                       |
|    - Input Guard: Prompt Injection Defense & PII/Secret Masking       |
|    - Output Guard: Destructive Command Interception (rm -rf, drops)   |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 3. Multi-Agent Control Harness (`agents/`)                            |
|    - Triage Agent: Invokes `tools/` (Kubectl, DB Metrics)             |
|    - Handoff Controller: Manages state transitions between agents     |
|    - Remediation Agent: Formulates safe recovery strategy             |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| 4. Delivery Layer (`api.py` / `main.py`)                              |
|    - FastAPI REST Endpoint (`POST /incident`) & Interactive CLI       |
+-----------------------------------------------------------------------+