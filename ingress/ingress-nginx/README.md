# ingress-nginx

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Helm chart configuration planning for `ingress-nginx` on jAIMSnet DOKS cluster.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://kubernetes.github.io/ingress-nginx` |
| Chart | `ingress-nginx/ingress-nginx` |
| Namespace | `ingress-nginx` |
| Release name | `ingress-nginx` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `controller.service.type` | `LoadBalancer` | DigitalOcean managed LB |
| `controller.service.loadBalancerIP` | `129.212.240.75` | Reserved LB IP |
| `controller.replicaCount` | `1` → `2` in Phase 2 | HA in Phase 2 |
| `controller.metrics.enabled` | `false` → `true` in Phase 2 | Prometheus scrape in Phase 2 |
| `controller.config.use-forwarded-headers` | `"true"` | Preserve client IP behind LB |
| `controller.config.ssl-protocols` | `"TLSv1.2 TLSv1.3"` | Security hardening |

## Managed Ingress Routes

| Service | Host | Backend | Namespace |
|---|---|---|---|
| LiteLLM | `litellm.jAIMS.app` | `litellm:4000` | `gateway` |
| Langfuse | `langfuse.jAIMS.app` | `langfuse:3000` | `observability` |
| Uptime Kuma | `kuma.jAIMS.app` | `uptime-kuma:3001` | (Docker Droplet) |

## Related

- [cert-manager/README.md](../cert-manager/README.md) — TLS certificate automation
- [ADR-007](../../docs/decisions/007-caddy-vs-nginx-ingress.md) — ingress-nginx decision
