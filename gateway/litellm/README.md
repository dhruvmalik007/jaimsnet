# LiteLLM

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

LiteLLM is the AI gateway at the core of jAIMSnet — providing a unified OpenAI-compatible proxy for routing requests to multiple LLM providers, enforcing budgets, managing virtual keys, and logging to Langfuse.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://github.com/BerriAI/litellm/tree/main/deploy/charts/litellm-helm` |
| Chart | `litellm/litellm-helm` |
| Namespace | `gateway` |
| Release name | `litellm` |
| Ingress host | `litellm.jAIMS.app` |

## Configuration Planning

### Core Settings

| Parameter | Value | Notes |
|---|---|---|
| Database | DigitalOcean Managed PostgreSQL | ATL1, port 25060, sslmode=require |
| Cache | Redis (in-cluster) | See [redis/README.md](../redis/README.md) |
| Observability | Langfuse | Success/failure callback |
| Port | `4000` | Internal ClusterIP |

### Model Routing (Planned)

| Alias | Provider | Model | Phase |
|---|---|---|---|
| `gpt-4o` | OpenAI | `gpt-4o` | Phase 1 🔴 |
| `gpt-4o-mini` | OpenAI | `gpt-4o-mini` | Phase 1 🔴 |
| `claude-3-5-sonnet` | Anthropic | `claude-3-5-sonnet-20241022` | Phase 1 🔴 |
| `llama3-70b` | vLLM (GPU Droplet) | Custom endpoint | Phase 2 🟠 |
| `mistral-7b` | vLLM (GPU Droplet) | Custom endpoint | Phase 2 🟠 |

### Virtual Keys & Budgets (Planned)

| Key Name | Budget | Rate Limit | Assigned To |
|---|---|---|---|
| `sk-platform-internal` | No limit | No limit | Internal platform use |
| `sk-dev-team` | $50/month | 100 RPM | Development team |
| `sk-external-api` | $200/month | 500 RPM | External API consumers |

## Related

- [redis/README.md](../redis/README.md)
- [ADR-001](../../docs/decisions/001-litellm-over-alternatives.md)
- [docs/runbooks/litellm-operations.md](../../docs/runbooks/litellm-operations.md)
