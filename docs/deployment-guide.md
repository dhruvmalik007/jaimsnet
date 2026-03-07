# Deployment Guide

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Step-by-step deployment guide for jAIMSnet Phase 1 on DigitalOcean DOKS.

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| kubectl | 1.34+ | Cluster management |
| helm | 3.x | Chart deployments |
| tofu / terraform | 1.x | Infrastructure provisioning |
| infisical | latest | Secret management |
| doctl | latest | DigitalOcean CLI |

## Deployment Order

| Step | Component | Command Reference | Status |
|---|---|---|---|
| 1 | Provision DOKS cluster | OpenTofu - iac/opentofu/ | 🔄 In Progress |
| 2 | Deploy ingress-nginx | Helm - ingress/ingress-nginx/ | 🔄 In Progress |
| 3 | Deploy cert-manager | Helm - ingress/cert-manager/ | 🔄 In Progress |
| 4 | Deploy Infisical Operator | Helm - secrets/infisical/operator/ | 🔄 In Progress |
| 5 | Apply InfisicalSecret CRDs | kubectl - secrets/infisical/sync/ | �� In Progress |
| 6 | Deploy Redis | Helm - gateway/redis/ | 🔄 In Progress |
| 7 | Deploy LiteLLM | Helm - gateway/litellm/ | 🔄 In Progress |
| 8 | Deploy Langfuse | Helm - observability/langfuse/ | 🔄 In Progress |
| 9 | Verify all services | curl health checks | 🔄 In Progress |

## Verification

| Check | Command |
|---|---|
| Cluster nodes | kubectl get nodes |
| All pods running | kubectl get pods -A |
| LiteLLM health | curl https://litellm.jAIMS.app/health |
| Langfuse health | curl https://langfuse.jAIMS.app/api/public/health |
| TLS valid | curl -I https://litellm.jAIMS.app |

## Related

- [docs/runbooks/](./runbooks/) — Operational runbooks for each service
- [docs/architecture.md](./architecture.md) — System architecture
