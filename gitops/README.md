# GitOps

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

GitOps strategy for jAIMSnet: ArgoCD for Kubernetes workloads (push to Git = deploy to cluster), Watchtower for Docker Droplet container auto-updates.

## Components

| Directory | Tool | Scope | Phase | Status |
|---|---|---|---|---|
| [argocd/](./argocd/) | ArgoCD | K8s workload continuous delivery | Phase 3 🟡 | 📋 Planned |
| [watchtower/](./watchtower/) | Watchtower | Docker Droplet container auto-updates | Phase 3 🟡 | 📋 Planned |

## Workflow

| Step | Action |
|---|---|
| 1 | Developer opens PR with Helm value changes |
| 2 | CI validates (helm-lint, kubeconform, yamllint) |
| 3 | PR merged to main |
| 4 | ArgoCD detects change in Git, syncs to cluster |
| 5 | Deployment rolls out; health checked by ArgoCD |

## App-of-Apps Pattern

ArgoCD uses the App-of-Apps pattern. A root Application in the cluster points to
[gitops/argocd/applications/](./argocd/applications/), which contains one Application
manifest per workload.
