# Namespace Planning

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Kubernetes namespace layout for jAIMSnet on DOKS (`jaimsnet-cluster`, ATL1).

## Namespace Inventory

| Namespace | Purpose | Phase | Status |
|---|---|---|---|
| `gateway` | LiteLLM proxy + Redis cache | Phase 1 🔴 | 🔄 In Progress |
| `observability` | Langfuse LLM observability | Phase 1 🔴 | 🔄 In Progress |
| `infisical` | Infisical Operator + secret sync | Phase 1 🔴 | 🔄 In Progress |
| `ingress-nginx` | ingress-nginx controller | Phase 1 🔴 | 🔄 In Progress |
| `cert-manager` | cert-manager TLS automation | Phase 1 🔴 | 🔄 In Progress |
| `monitoring` | Prometheus + Grafana + Loki + Alloy + Mimir | Phase 2 🟠 | 📋 Planned |
| `security` | Kyverno, Falco, CrowdSec, Trivy Operator | Phase 3 🟡 | 📋 Planned |

## Labels & Conventions

| Label | Value | Purpose |
|---|---|---|
| `app.kubernetes.io/managed-by` | `helm` | Helm-managed resources |
| `jaimsnet.io/phase` | `phase-1`, `phase-2`, etc. | Phase tracking |
| `jaimsnet.io/owner` | `@SHD`, `@RMN`, etc. | Team ownership |

## Notes

- All namespaces are created via OpenTofu or Helm pre-install hooks
- Network policies (Phase 2, Cilium) will restrict cross-namespace traffic
- See [network-policies.md](./network-policies.md) for Cilium CNI planning
