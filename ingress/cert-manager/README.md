# cert-manager

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Helm chart configuration planning for `cert-manager` on jAIMSnet DOKS cluster. Automates TLS certificate provisioning via Let's Encrypt.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://charts.jetstack.io` |
| Chart | `jetstack/cert-manager` |
| Namespace | `cert-manager` |
| Release name | `cert-manager` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `installCRDs` | `true` | Install cert-manager CRDs |
| `global.leaderElection.namespace` | `cert-manager` | HA leader election |
| `prometheus.enabled` | `false` → `true` Phase 2 | Metrics in Phase 2 |

## ClusterIssuer Planning

| Issuer | Type | Server | Used For |
|---|---|---|---|
| `letsencrypt-staging` | ACME HTTP-01 | Let's Encrypt Staging | Testing |
| `letsencrypt-prod` | ACME HTTP-01 | Let's Encrypt Production | `*.jaims.app` |

### ACME Configuration Notes

- Challenge type: HTTP-01 via ingress-nginx
- Contact email: ops@jaims.app (placeholder — update before deploy)
- Wildcard cert (`*.jaims.app`) requires DNS-01 challenge — planned for Phase 2 with DigitalOcean DNS provider

## Certificates

| Certificate | Namespace | Domains | Issuer |
|---|---|---|---|
| `litellm-tls` | `gateway` | `litellm.jAIMS.app` | `letsencrypt-prod` |
| `langfuse-tls` | `observability` | `langfuse.jAIMS.app` | `letsencrypt-prod` |

## Related

- [ingress-nginx/README.md](../ingress-nginx/README.md)
- [ADR-007](../../docs/decisions/007-caddy-vs-nginx-ingress.md)
