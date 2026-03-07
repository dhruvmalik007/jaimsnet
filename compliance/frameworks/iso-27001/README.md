# ISO 27001:2022

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

ISO 27001:2022 Information Security Management System (ISMS) planning for jAIMSnet. The 2022 revision reorganized Annex A into 4 themes (Organizational, People, Physical, Technological) with 93 controls.

## Annex A Theme Summary

| Theme | Controls | Description |
|---|---|---|
| Organizational | A.5 (37 controls) | Policies, roles, responsibilities, supplier management |
| People | A.6 (8 controls) | HR security, awareness, remote work |
| Physical | A.7 (14 controls) | Physical access, equipment, clear desk |
| Technological | A.8 (34 controls) | Access control, encryption, ops security, vulnerability mgmt |

## Key Control Mappings (Technological)

| Control | Description | jAIMSnet Implementation | Status |
|---|---|---|---|
| A.8.2 | Privileged access rights | K8s RBAC, Infisical access control | 🔄 In Progress |
| A.8.5 | Secure authentication | Infisical Kubernetes Auth, no static tokens | 🔄 In Progress |
| A.8.7 | Protection against malware | Trivy, Falco, CrowdSec | 📋 Planned |
| A.8.8 | Management of technical vulnerabilities | Trivy Operator, Grype, CI scans | 📋 Planned |
| A.8.9 | Configuration management | kube-bench, docker-bench, Kyverno | 📋 Planned |
| A.8.12 | Data leakage prevention | Gitleaks, network policies | 📋 Planned |
| A.8.16 | Monitoring activities | Falco, Loki, Prometheus | 📋 Planned |
| A.8.24 | Use of cryptography | TLS everywhere, DB sslmode=require | 🔄 In Progress |
| A.8.25 | Secure development lifecycle | CI pipeline, ADRs, Trivy in CI | 📋 Planned |

## ISMS Scope Statement (Draft)

> The jAIMSnet ISMS covers the AI infrastructure management platform, including the LLM gateway (LiteLLM), AI observability (Langfuse), GPU inference infrastructure (vLLM), and supporting Kubernetes and DigitalOcean cloud infrastructure, operated by the jAIMSnet organization.
