# Network Policies (Cilium)

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Cilium CNI network policy planning for jAIMSnet. Default-deny posture with explicit allow rules per namespace.

## Planned Policies

| Policy | Namespace | Direction | Allowed | Phase | Status |
|---|---|---|---|---|---|
| `gateway-ingress` | `gateway` | Ingress | `ingress-nginx` → `litellm:4000` | Phase 2 🟠 | ⬜ TODO |
| `gateway-egress` | `gateway` | Egress | `litellm` → PostgreSQL, external LLM APIs | Phase 2 🟠 | ⬜ TODO |
| `observability-ingress` | `observability` | Ingress | `ingress-nginx` → `langfuse:3000` | Phase 2 🟠 | ⬜ TODO |
| `observability-egress` | `observability` | Egress | `langfuse` → PostgreSQL | Phase 2 🟠 | ⬜ TODO |
| `infisical-egress` | `infisical` | Egress | Operator → Infisical Cloud API | Phase 2 🟠 | ⬜ TODO |
| `default-deny` | All | Both | Deny all unlisted traffic | Phase 2 🟠 | ⬜ TODO |

## Implementation Notes

- Cilium will replace the default DOKS CNI in Phase 2
- CiliumNetworkPolicy CRDs extend standard K8s NetworkPolicy with L7 visibility
- DNS-based egress policies will be used for external API calls
- Hubble UI will provide network flow visibility
