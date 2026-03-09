# Redis

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Redis provides in-cluster caching for LiteLLM — reducing LLM API costs by serving identical requests from cache and enabling rate limiting across instances.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://charts.bitnami.com/bitnami` |
| Chart | `bitnami/redis` |
| Namespace | `gateway` |
| Release name | `redis` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `architecture` | `standalone` | Single replica for Phase 1 |
| `auth.enabled` | `true` | Redis password via Infisical |
| `persistence.enabled` | `true` | Survive pod restarts |
| `persistence.size` | `8Gi` | Initial size |
| `resources.requests.memory` | `256Mi` | Base memory |
| `resources.limits.memory` | `1Gi` | Max memory for cache |

## Usage by LiteLLM

| Feature | Redis Usage |
|---|---|
| Response caching | Cache identical prompts + params |
| Rate limiting | Per-key RPM/TPM enforcement |
| Request deduplication | Prevent duplicate in-flight requests |

## Related

- [litellm/README.md](../litellm/README.md)
