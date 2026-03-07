# Architecture Decision Records (ADRs)

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

ADRs capture significant architectural decisions made during the design and development of jAIMSnet. Each record documents the context, options considered, decision made, and consequences.

## ADR Index

| # | Title | Status | Date | Owner |
|---|---|---|---|---|
| 001 | [LiteLLM Over Alternatives](./001-litellm-over-alternatives.md) | ✅ Accepted | 2025-01-01 | @RMN |
| 002 | [Langfuse Over Phoenix](./002-langfuse-over-phoenix.md) | ✅ Accepted | 2025-01-01 | @RMN |
| 003 | [DOKS Over Self-Managed Droplet](./003-doks-over-droplet.md) | ✅ Accepted | 2025-01-01 | @SHD |
| 004 | [Infisical for Secrets Management](./004-infisical-for-secrets.md) | ✅ Accepted | 2025-01-01 | @SHD |
| 005 | [Monorepo Structure](./005-monorepo-structure.md) | ✅ Accepted | 2025-01-01 | @RMN |
| 006 | [vLLM Over SGLang for GPU Inference](./006-vllm-over-sglang.md) | ✅ Accepted | 2025-01-01 | @LDC |
| 007 | [ingress-nginx Over Caddy](./007-caddy-vs-nginx-ingress.md) | ✅ Accepted | 2025-01-01 | @SHD |

## ADR Template

```markdown
# ADR-NNN: Title

| Field | Value |
|---|---|
| **Status** | Proposed / Accepted / Deprecated / Superseded |
| **Date** | YYYY-MM-DD |
| **Owner** | @handle |
| **Deciders** | @handle1, @handle2 |

## Context

<!-- What is the issue that motivates this decision? -->

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| Option A | ... | ... |
| Option B | ... | ... |

## Decision

<!-- What was decided? -->

## Consequences

### Positive
- ...

### Negative / Trade-offs
- ...

## References
- ...
```
