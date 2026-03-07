# Ingress

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Ingress configuration for jAIMSnet — ingress-nginx as the Kubernetes ingress controller with cert-manager for automated TLS via Let's Encrypt. Traffic enters via DigitalOcean Load Balancer IP 129.212.240.75.

## Components

| Component | Directory | Purpose | Phase | Status |
|---|---|---|---|---|
| ingress-nginx | [ingress-nginx/](./ingress-nginx/) | HTTP/HTTPS routing, LB integration | Phase 1 🔴 | 🔄 In Progress |
| cert-manager | [cert-manager/](./cert-manager/) | TLS certificate automation (Let's Encrypt) | Phase 1 🔴 | 🔄 In Progress |

## Domain Routing

| Domain | Backend | Namespace | TLS |
|---|---|---|---|
| litellm.jAIMS.app | litellm:4000 | gateway | Let's Encrypt |
| langfuse.jAIMS.app | langfuse:3000 | observability | Let's Encrypt |
| kuma.jAIMS.app | uptime-kuma:3001 | Docker Droplet | Caddy |

## Related

- [ADR-007](../docs/decisions/007-caddy-vs-nginx-ingress.md) — ingress-nginx decision
