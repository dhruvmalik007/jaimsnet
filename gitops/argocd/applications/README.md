# ArgoCD Application Manifests

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

ArgoCD `Application` CRD manifests for each jAIMSnet workload. Uses the App-of-Apps pattern — a root Application points to this directory.

## Planned Applications

| Application | Namespace | Chart Source | Phase | Status |
|---|---|---|---|---|
| `litellm` | `gateway` | `gateway/litellm/` | Phase 3 🟡 | ⬜ TODO |
| `redis` | `gateway` | `gateway/redis/` | Phase 3 🟡 | ⬜ TODO |
| `langfuse` | `observability` | `observability/langfuse/` | Phase 3 🟡 | ⬜ TODO |
| `infisical-operator` | `infisical` | `secrets/infisical/operator/` | Phase 3 🟡 | ⬜ TODO |
| `ingress-nginx` | `ingress-nginx` | `ingress/ingress-nginx/` | Phase 3 🟡 | ⬜ TODO |
| `cert-manager` | `cert-manager` | `ingress/cert-manager/` | Phase 3 🟡 | ⬜ TODO |
| `kyverno` | `security` | `security/kyverno/` | Phase 3 🟡 | ⬜ TODO |

## Sync Policies

| Policy | Value |
|---|---|
| Auto-sync | Enabled |
| Self-heal | Enabled |
| Prune | Enabled (removes deleted resources) |
| Sync waves | Ordered: infra → secrets → apps |
