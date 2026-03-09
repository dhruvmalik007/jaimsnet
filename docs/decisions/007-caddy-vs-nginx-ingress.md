# ADR-007: ingress-nginx Over Caddy for Kubernetes Ingress

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @SHD |
| **Deciders** | @SHD, @RMN |

## Context

jAIMSnet services (LiteLLM, Langfuse, Uptime Kuma) need TLS termination and HTTP routing within the DOKS cluster. A Kubernetes-native ingress controller must be chosen to route external traffic to internal services.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **ingress-nginx** | Kubernetes standard, widely adopted, extensive annotation support, CrowdSec integration, DigitalOcean LB native, cert-manager integration | Configuration via annotations can be verbose |
| **Caddy** | Automatic HTTPS, simple config, low resource usage | Not a native K8s ingress controller; requires additional setup in K8s; less ecosystem integration |
| **Traefik** | CRD-based config, middleware support, dashboard | More complex setup; CRD overhead |
| **Istio Gateway** | Full service mesh, advanced traffic management | Overkill for Phase 1; high resource overhead |

## Decision

Use **ingress-nginx** deployed via Helm with a DigitalOcean Load Balancer as the external entry point (IP: `129.212.240.75`). cert-manager handles TLS certificate provisioning via Let's Encrypt.

## Configuration Notes

| Component | Detail |
|---|---|
| Helm chart | `ingress-nginx/ingress-nginx` |
| Load Balancer IP | `129.212.240.75` |
| TLS provider | cert-manager + Let's Encrypt |
| Wildcard cert | `*.jaims.app` |
| CrowdSec integration | Phase 3 (bouncer plugin) |

## Consequences

### Positive
- First-class DigitalOcean LB integration
- cert-manager ClusterIssuer works natively with ingress-nginx annotations
- CrowdSec Bouncer plugin available as ingress-nginx middleware (Phase 3)
- Large community, well-documented for DOKS

### Negative / Trade-offs
- Caddy's automatic HTTPS is simpler, but not Kubernetes-native
- ingress-nginx requires separate cert-manager installation

## References
- [ingress-nginx Documentation](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [ingress/ingress-nginx/README.md](../../ingress/ingress-nginx/README.md)
- [ingress/cert-manager/README.md](../../ingress/cert-manager/README.md)
