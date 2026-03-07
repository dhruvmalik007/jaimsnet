# ADR-001: LiteLLM Over Alternatives

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @RMN |
| **Deciders** | @RMN, @LDC |

## Context

jAIMSnet requires an LLM gateway to provide a unified API for routing requests to multiple LLM providers (OpenAI, Anthropic, self-hosted vLLM), with virtual key management, budget enforcement, and observability integration.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **LiteLLM** | OpenAI-compatible API, 100+ provider support, virtual keys, budgets, Langfuse integration, active community, Helm chart | Self-hosted, requires PostgreSQL |
| OpenRouter | Hosted, simple integration | No self-hosted option, vendor lock-in, no budget controls |
| AWS Bedrock Gateway | AWS-native | AWS lock-in, limited provider support, no budget controls |
| Custom proxy | Full control | High development cost, maintenance burden |

## Decision

Use **LiteLLM** deployed via Helm on DOKS as the primary AI gateway.

## Consequences

### Positive
- Single API endpoint for all LLM providers
- Virtual keys enable per-team/project budget enforcement
- Native Langfuse callback for full observability
- Reduces provider coupling — swap providers without client changes

### Negative / Trade-offs
- Requires self-hosted PostgreSQL (mitigated by DigitalOcean Managed PG)
- Adds operational complexity vs. direct provider APIs

## References
- [LiteLLM Documentation](https://docs.litellm.ai)
- [gateway/litellm/README.md](../../gateway/litellm/README.md)
