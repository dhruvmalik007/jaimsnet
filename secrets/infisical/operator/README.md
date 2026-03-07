# Infisical Operator

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Helm chart configuration planning for the Infisical Kubernetes Operator. The operator watches `InfisicalSecret` CRDs and syncs secrets from Infisical Cloud into Kubernetes `Secret` objects.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://dl.cloudsmith.io/public/infisical/helm-charts/` |
| Chart | `infisical-helm-charts/secrets-operator` |
| Namespace | `infisical` |
| Release name | `infisical-operator` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `image.tag` | Latest stable | Pin version before deploy |
| `resources.requests.cpu` | `50m` | Minimal CPU |
| `resources.requests.memory` | `64Mi` | Minimal memory |
| `controllerManager.manager.env.INFISICAL_URL` | `https://app.infisical.com` | Infisical Cloud endpoint |

## Authentication

Uses **Kubernetes Auth** — the operator authenticates to Infisical using the pod's service account token. No static credentials are stored in the cluster.

| Component | Value |
|---|---|
| Auth method | Kubernetes Auth |
| Service account | `infisical-operator` (auto-created) |
| Infisical machine identity | Configured in Infisical Cloud Pro |

## Related

- [sync/README.md](../sync/README.md) — InfisicalSecret CRD definitions
- [ADR-004](../../../docs/decisions/004-infisical-for-secrets.md)
