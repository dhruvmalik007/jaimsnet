# Gateway

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

The jAIMSnet AI gateway provides a unified, OpenAI-compatible API for routing LLM requests across multiple providers, with caching, rate limiting, virtual keys, budget enforcement, and Langfuse observability.

## Components

| Component | Directory | Purpose | Phase | Status |
|---|---|---|---|---|
| LiteLLM | [litellm/](./litellm/) | LLM proxy gateway, routing, budgets | Phase 1 🔴 | 🔄 In Progress |
| Redis | [redis/](./redis/) | Response caching, rate limiting | Phase 1 �� | 🔄 In Progress |

## Endpoint

| Service | URL | Protocol |
|---|---|---|
| LiteLLM API | https://litellm.jAIMS.app | HTTPS, OpenAI-compatible |

## Related

- [ADR-001](../docs/decisions/001-litellm-over-alternatives.md) — LiteLLM decision
- [docs/runbooks/litellm-operations.md](../docs/runbooks/litellm-operations.md)
