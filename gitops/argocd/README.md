# ArgoCD

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

ArgoCD provides GitOps-based continuous delivery for all Kubernetes workloads in jAIMSnet. Changes merged to `main` are automatically applied to the cluster.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://argoproj.github.io/argo-helm` |
| Chart | `argo/argo-cd` |
| Namespace | `argocd` |
| Release name | `argocd` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `server.ingress.enabled` | `true` | Expose via ingress-nginx |
| `server.ingress.hostname` | `argocd.jAIMS.app` | Phase 3 |
| `configs.params.server.insecure` | `true` | TLS handled by ingress |
| RBAC | GitHub SSO via Dex | Phase 3 |
| Auto-sync | Enabled for all apps | GitOps workflow |
| Self-heal | Enabled | Revert manual changes |

## App-of-Apps Pattern

ArgoCD will use the App-of-Apps pattern:
- Root Application points to `gitops/argocd/applications/`
- Each Application manifest in that directory manages one workload

## Related

- [applications/README.md](./applications/README.md)
- [../watchtower/README.md](../watchtower/README.md)
