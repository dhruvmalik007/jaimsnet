# ADR-004: Infisical for Secrets Management

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @SHD |
| **Deciders** | @SHD, @RMN |

## Context

jAIMSnet requires a secrets management solution for API keys, database credentials, and service tokens. Secrets must be accessible in Kubernetes without being stored in Git, and auditable for compliance.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Infisical Cloud Pro** | K8s Operator, Kubernetes Auth (no static tokens), audit logs, SOC 2 compliant, UI + CLI | SaaS dependency, cost |
| HashiCorp Vault | Gold standard, self-hosted possible | High ops overhead, complex HA setup |
| AWS Secrets Manager | Hosted, HA | AWS lock-in, cost at scale |
| Sealed Secrets | Git-friendly encrypted secrets | Cannot rotate without redeployment, no audit trail |
| External Secrets Operator | Flexible backend support | Requires separate secrets backend |

## Decision

Use **Infisical Cloud Pro** with the Infisical Kubernetes Operator for all jAIMSnet secrets.

## Authentication Method

Kubernetes Auth is used exclusively — the Infisical Operator authenticates using the pod service account JWT token. No static Infisical access tokens are stored in the cluster.

## Consequences

### Positive
- Zero static secrets in cluster or Git
- Full audit trail in Infisical Cloud (SOC 2 CC6.1 evidence)
- InfisicalSecret CRDs provide declarative secret sync
- Infisical Cloud Pro: RBAC, environments, secret versioning
- Rotation: update in Infisical UI, operator re-syncs automatically

### Negative / Trade-offs
- Dependency on Infisical Cloud availability (mitigated by caching)
- SaaS cost (Pro plan)

## References
- [secrets/infisical/README.md](../../secrets/infisical/README.md)
- [Infisical K8s Operator](https://infisical.com/docs/integrations/platforms/kubernetes)
- [docs/runbooks/secret-rotation.md](../../docs/runbooks/secret-rotation.md)
