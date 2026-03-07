# SOC 2 Type II

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN + @GTM |
| **Last Updated** | 2025-01-01 |

SOC 2 Type II audit planning for jAIMSnet. SOC 2 evaluates controls relevant to the Trust Service Criteria (TSC) over a defined observation period (typically 6–12 months).

## Trust Service Criteria

| Criteria | Code | Description | Phase |
|---|---|---|---|
| Security | CC | Common Criteria (required) | Phase 3 🟡 |
| Availability | A | System availability SLAs | Phase 3 🟡 |
| Confidentiality | C | Protection of confidential data | Phase 3 🟡 |
| Processing Integrity | PI | Complete, accurate processing | Phase 4 🟢 |
| Privacy | P | Personal information handling | Phase 4 🟢 |

## Common Criteria (CC) Key Mapping

| CC ID | Description | jAIMSnet Control | Status |
|---|---|---|---|
| CC1.1 | Board/management oversight | GitHub org governance, ADRs | 📋 Planned |
| CC2.1 | Risk assessment | Compliance framework, ADRs | 📋 Planned |
| CC6.1 | Logical access controls | K8s RBAC, Infisical | 🔄 In Progress |
| CC6.3 | Role-based access | CODEOWNERS, Infisical RBAC | 🔄 In Progress |
| CC6.6 | Boundary protection | VPC, Cilium, CrowdSec | Phase 2–3 |
| CC6.7 | Transmission protection | TLS, sslmode=require | 🔄 In Progress |
| CC6.8 | Vulnerability management | Trivy, Grype, CI scans | Phase 3 🟡 |
| CC7.1 | Detection and monitoring | Falco, Prometheus, Loki | Phase 2–3 |
| CC7.2 | Incident response | incident-response.md | 🔄 In Progress |
| CC7.3 | Backup | PG backups, DR runbook | Phase 1 |
| CC8.1 | Change management | GitHub PRs, CODEOWNERS, CI | Phase 1–3 |
| CC9.1 | Risk mitigation | ADRs, compliance policies | 📋 Planned |

## Evidence Collection Plan

| Control | Evidence Source | Frequency |
|---|---|---|
| Access reviews | K8s RBAC audit, Infisical logs | Quarterly |
| Vulnerability scans | Trivy, Grype reports | Monthly |
| Incident records | GitHub Issues, runbook logs | Per incident |
| Change management | GitHub PR history | Continuous |
| Uptime/availability | Uptime Kuma reports | Monthly |
| Backup testing | DR runbook execution | Quarterly |
