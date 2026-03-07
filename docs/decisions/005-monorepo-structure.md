# ADR-005: Monorepo Structure for jAIMSnet

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @RMN |
| **Deciders** | @RMN, @SHD, @LDC |

## Context

jAIMSnet spans multiple infrastructure domains: Kubernetes cluster config, Helm values, IaC (OpenTofu), Ansible playbooks, CI/CD workflows, security policies, compliance documentation, and observability config. A decision was needed on whether to split these into separate repositories or maintain them in a single monorepo.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Monorepo** | Single source of truth, atomic cross-cutting changes, unified CI, shared ADRs and docs | Can grow large; requires good directory discipline |
| **Polyrepo (per-service)** | Clear ownership boundaries, smaller PRs per area | Cross-cutting changes require multiple PRs; harder to see system state |
| **Polyrepo (by tier)** | Mid-ground grouping (infra, app, ops) | Still splits context across repos |

## Decision

Adopt a **monorepo** structure with clear top-level directories per domain. Each directory has a README.md documenting its purpose, phase, owner, and status. Implementation files (Helm values, TF modules, manifests) live alongside their documentation.

## Directory Structure

| Directory | Domain | Owner |
|---|---|---|
| `cluster/` | DOKS cluster config | @SHD |
| `gateway/` | LiteLLM + Redis | @RMN |
| `observability/` | Langfuse + Prometheus stack | @RMN |
| `ingress/` | ingress-nginx + cert-manager | @SHD |
| `secrets/` | Infisical operator + sync | @SHD |
| `gpu/` | vLLM on MI300X | @LDC |
| `iac/` | OpenTofu + Ansible | @LDC |
| `gitops/` | ArgoCD + Watchtower | @SHD |
| `security/` | Kyverno, Trivy, Falco, CrowdSec | @SHD |
| `compliance/` | Frameworks, policies, evidence | @RMN |
| `testing/` | Integration, load, chaos | @LDC |
| `docs/` | Architecture, ADRs, runbooks | @RMN |
| `scripts/` | Utility scripts | @SHD |

## Consequences

### Positive
- Single PR can update Helm values, related docs, and CI config atomically
- Compliance evidence collection can reference a unified commit history
- Onboarding is simplified — one repo to clone
- CODEOWNERS enforces per-directory ownership

### Negative / Trade-offs
- Repository will grow over time; requires discipline to avoid sprawl
- CI pipelines must be path-filtered to avoid unnecessary runs

## References
- [GitHub CODEOWNERS](../../.github/CODEOWNERS)
- [Monorepo vs Polyrepo — Thoughtworks](https://www.thoughtworks.com/insights/blog/monorepo-vs-polyrepo)
