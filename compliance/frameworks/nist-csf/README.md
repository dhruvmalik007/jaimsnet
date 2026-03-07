# NIST CSF 2.0

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

NIST Cybersecurity Framework 2.0 control mapping for jAIMSnet. CSF 2.0 introduced the **Govern** function alongside the original five functions.

## Function Mapping

| Function | Subcategories | jAIMSnet Controls | Phase |
|---|---|---|---|
| **GV — Govern** | Roles, policies, oversight | CODEOWNERS, ADRs, compliance policies | Phase 3 🟡 |
| **ID — Identify** | Asset mgmt, risk assessment | OpenTofu inventory, Trivy SBOM | Phase 3 🟡 |
| **PR — Protect** | Access control, hardening | Infisical, Kyverno, CIS Benchmarks, Cilium | Phase 2–3 |
| **DE — Detect** | Monitoring, anomaly detection | Falco, CrowdSec, Prometheus + Grafana | Phase 2–3 |
| **RS — Respond** | Incident response | Runbooks, incident-response.md | Phase 1–3 |
| **RC — Recover** | Recovery planning | Disaster recovery runbook, DB backups | Phase 1–3 |

## Key Subcategory Mappings

| CSF ID | Subcategory | jAIMSnet Implementation | Status |
|---|---|---|---|
| GV.OC-01 | Mission and objectives | README.md, docs/architecture.md | 🔄 In Progress |
| ID.AM-01 | Asset inventory | OpenTofu state, SBOM (Syft) | 📋 Planned |
| PR.AA-01 | Identity management | Infisical (secrets), K8s RBAC | Phase 1 |
| PR.DS-01 | Data at rest protection | DB encryption, TLS | Phase 1 |
| DE.CM-01 | Network monitoring | Cilium Hubble, Falco | Phase 2–3 |
| RS.MA-01 | Incident management | incident-response.md | Phase 1 |
| RC.RP-01 | Recovery planning | disaster-recovery.md | Phase 1 |
