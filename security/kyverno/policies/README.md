# Kyverno Policies

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

ClusterPolicy definitions for jAIMSnet Kubernetes workload governance.

## Policy Index

| Policy | File | Type | Action | Phase | Status |
|---|---|---|---|---|---|
| Require Labels | `require-labels.yaml` | Validation | Enforce | Phase 2 🟠 | ⬜ TODO |
| Require Resource Limits | `require-resource-limits.yaml` | Validation | Enforce | Phase 2 🟠 | ⬜ TODO |
| Disallow Privileged | `disallow-privileged.yaml` | Validation | Enforce | Phase 2 🟠 | ⬜ TODO |
| Require Non-Root | `require-non-root.yaml` | Validation | Enforce | Phase 2 🟠 | ⬜ TODO |
| Restrict Image Registries | `restrict-image-registries.yaml` | Validation | Audit → Enforce | Phase 2 🟠 | ⬜ TODO |

## Required Labels

All workloads must include:

| Label | Purpose |
|---|---|
| `app.kubernetes.io/name` | Application name |
| `app.kubernetes.io/version` | Image version |
| `jaimsnet.io/owner` | Team owner handle |
| `jaimsnet.io/phase` | Deployment phase |

## Rollout Strategy

Policies will start in **Audit** mode during Phase 2, then move to **Enforce** after all existing workloads comply.
