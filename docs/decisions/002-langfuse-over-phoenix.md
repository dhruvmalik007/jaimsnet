# ADR-002: Langfuse Over Phoenix for LLM Observability

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @RMN |
| **Deciders** | @RMN, @LDC |

## Context

jAIMSnet requires LLM-specific observability: trace logging, cost tracking, prompt/response capture, and evaluation support. Standard APM tools do not provide LLM-aware primitives.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Langfuse** | Open source, self-hosted, LiteLLM native integration, ISO 42001 trace evidence, evals, cost tracking, Helm chart | Requires PostgreSQL |
| Arize Phoenix | Strong evals, open source | Less mature Helm/K8s support at decision time |
| LangSmith | Feature-rich | Hosted-only, vendor lock-in, cost |
| Helicone | Simple | Limited eval/trace depth |

## Decision

Use **Langfuse** deployed via Helm on DOKS as the LLM observability platform.

## Consequences

### Positive
- LiteLLM success/failure callback sends traces automatically
- Provides ISO 42001 A.6.2 evidence (AI system recording)
- Self-hosted: data sovereignty for sensitive LLM interactions
- Cost dashboard feeds LiteLLM budget decisions

### Negative / Trade-offs
- Requires PostgreSQL (shared with LiteLLM on managed PG)
- Self-hosted adds operational overhead vs. hosted alternatives

## References
- [Langfuse Documentation](https://langfuse.com/docs)
- [observability/langfuse/README.md](../../observability/langfuse/README.md)
- [compliance/frameworks/iso-42001/README.md](../../compliance/frameworks/iso-42001/README.md)
