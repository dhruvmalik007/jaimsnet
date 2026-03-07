# CSA CCM v4 — Cloud Controls Matrix

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Cloud Security Alliance (CSA) Cloud Controls Matrix v4 mapping for jAIMSnet. CCM v4 provides 197 control specifications across 17 domains specifically for cloud services.

## Domain Coverage

| Domain | Code | Description | jAIMSnet Relevance |
|---|---|---|---|
| Application & Interface Security | AIS | Secure SDLC, API security | LiteLLM API, CI pipeline |
| Audit Assurance & Compliance | AAC | Audit logging, compliance programs | Loki, compliance/ |
| Business Continuity | BCR | DR, backup, resilience | disaster-recovery.md |
| Change Control & Configuration | CCC | Change management, config | GitHub PRs, kube-bench |
| Cryptography, Encryption & Key Mgmt | CEK | TLS, key management | Infisical, TLS everywhere |
| Data Security & Privacy | DSP | Data classification, retention | PG encryption, sslmode |
| Governance & Risk | GRC | Risk management, policies | ADRs, compliance policies |
| Human Resources Security | HRS | Personnel security | Out of scope (platform) |
| Identity & Access Mgmt | IAM | Authentication, authorization | Infisical, K8s RBAC |
| Infrastructure & Virtualization | IVS | Hypervisor, container security | Kyverno, Falco |
| Interoperability & Portability | IPY | Cloud portability | DigitalOcean + standard K8s |
| Logging & Monitoring | LOG | SIEM, audit trails | Loki, Alloy, Falco |
| Network Security | NET | Firewalls, segmentation | Cilium, VPC, CrowdSec |
| Security Incident Mgmt | SEF | Incident response | incident-response.md |
| Supply Chain Mgmt | STA | Vendor security | Trivy, SBOM, Grype |
| Threat & Vulnerability Mgmt | TVM | CVE management | Trivy, kube-bench |
| Universal Endpoint Management | UEM | Device management | Droplet hardening (Ansible) |
