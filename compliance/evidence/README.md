# Evidence Collection

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Strategy for collecting and organizing compliance evidence from automated tools across the jAIMSnet platform.

## Tool-to-Evidence Mapping

| Tool | Evidence Type | Compliance Frameworks | Collection Method | Phase |
|---|---|---|---|---|
| Trivy Operator | Vulnerability management reports | SOC2 CC6.8, ISO 27001 A.8.8, CIS Control 7 | K8s CRDs → JSON export | Phase 3 🟡 |
| Falco | Intrusion detection alerts | SOC2 CC7.2, ISO 27001 A.8.16, NIST DE.CM-1 | Falcosidekick → Loki | Phase 3 🟡 |
| kube-bench | K8s CIS Benchmark results | CIS K8s Benchmark, SOC2 CC6.1, ISO 27001 A.8.9 | K8s Job → JSON | Phase 3 🟡 |
| docker-bench | Docker CIS Benchmark results | CIS Docker Benchmark, SOC2 CC6.1 | Ansible → JSON | Phase 3 🟡 |
| Gitleaks | Secret scanning (no secrets in Git) | SOC2 CC6.1, ISO 27001 A.8.12 | CI workflow → SARIF | Phase 3 🟡 |
| Infisical | Secret access audit logs | SOC2 CC6.1, ISO 27001 A.8.5 | Infisical Cloud audit export | Phase 1 🔴 |
| Langfuse | AI system monitoring, trace logs | ISO 42001 A.6.2, A.8.4 | Langfuse export / API | Phase 1 🔴 |
| LiteLLM | AI cost/usage tracking | ISO 42001 A.4.4, A.6.2 | LiteLLM DB + metrics | Phase 1 🔴 |
| GitHub PR history | Change management evidence | SOC2 CC8.1, ISO 27001 A.8.32 | GitHub API export | Phase 1 🔴 |
| Uptime Kuma | Availability records | SOC2 Availability TSC | Status page history | Phase 1 🔴 |

## Evidence Storage

| Type | Location | Retention |
|---|---|---|
| Raw evidence (JSON, logs) | `compliance/evidence/raw/` (gitignored) | 1 year |
| Summarized reports | `compliance/evidence/reports/` | Permanent |
| Audit findings | GitHub Issues (tagged `compliance`) | Permanent |

> **Note:** Raw evidence is excluded from Git via `.gitignore` (`/compliance/evidence/raw/`). Processed summaries and reports are committed.
