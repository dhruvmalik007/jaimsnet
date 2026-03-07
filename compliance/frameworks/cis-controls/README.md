# CIS Controls v8

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

CIS Controls v8 mapping for jAIMSnet. CIS Controls provide prioritized, actionable safeguards organized into Implementation Groups (IG1–IG3). jAIMSnet targets IG2 minimum.

## Implementation Group Target

| Group | Description | Target |
|---|---|---|
| IG1 | Essential cyber hygiene (all orgs) | ✅ Phase 1–2 |
| IG2 | For orgs with moderate security resources | ✅ Phase 2–3 |
| IG3 | For sophisticated security programs | 📋 Phase 3–4 |

## Control Mapping

| CIS Control | Description | jAIMSnet Implementation | Phase | Status |
|---|---|---|---|---|
| 1 — Inventory & Control of Enterprise Assets | Asset inventory | OpenTofu state, SBOM (Syft/Grype) | Phase 3 🟡 | 📋 Planned |
| 2 — Inventory & Control of Software Assets | Software inventory | Trivy SBOM reports | Phase 3 🟡 | 📋 Planned |
| 3 — Data Protection | Encryption at rest + transit | DB TLS, K8s secrets encryption | Phase 1 🔴 | 🔄 In Progress |
| 4 — Secure Configuration | CIS Benchmarks | kube-bench, docker-bench | Phase 3 🟡 | 📋 Planned |
| 5 — Account Management | IAM | K8s RBAC, Infisical access control | Phase 1 🔴 | 🔄 In Progress |
| 6 — Access Control | Least privilege | Kyverno policies, RBAC | Phase 2 🟠 | 📋 Planned |
| 7 — Vulnerability Management | CVE scanning | Trivy Operator, Grype | Phase 3 🟡 | 📋 Planned |
| 8 — Audit Log Management | Centralized logging | Loki + Alloy | Phase 2 🟠 | 📋 Planned |
| 9 — Email & Web Browser Protections | WAF | CrowdSec | Phase 3 🟡 | 📋 Planned |
| 12 — Network Infrastructure Management | Network segmentation | Cilium, VPC, NetworkPolicies | Phase 2 🟠 | 📋 Planned |
| 13 — Network Monitoring & Defense | IDS | Falco, CrowdSec | Phase 3 🟡 | 📋 Planned |
| 16 — Application Software Security | Secure dev | Gitleaks, Trivy, SBOM in CI | Phase 3 🟡 | 📋 Planned |
