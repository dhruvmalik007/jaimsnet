# Infisical — Secret Management

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

jAIMSnet uses [Infisical Cloud Pro](https://infisical.com) as the single source of truth for all secrets. The Infisical Kubernetes Operator syncs secrets into cluster namespaces via `InfisicalSecret` CRDs using Kubernetes Auth (no static tokens in the cluster).

## Architecture

```
Infisical Cloud Pro
    └── jAIMSnet Project
          ├── /gateway/litellm     → gateway namespace
          ├── /observability/      → observability namespace
          └── /infisical/operator  → infisical namespace
```

## Secret Inventory

| Secret Path | Kubernetes Secret | Namespace | Contains |
|---|---|---|---|
| `/gateway/litellm` | `litellm-secrets` | `gateway` | LiteLLM master key, DB URL, Redis URL, provider API keys |
| `/observability/langfuse` | `langfuse-secrets` | `observability` | Langfuse secret key, DB URL, NextAuth secret |
| `/infisical/operator` | `infisical-operator-credentials` | `infisical` | Infisical service token for operator auth |

## Security Notes

- All secrets use **Kubernetes Auth** — no static Infisical tokens in cluster manifests
- Secrets are never committed to Git (see `.gitignore`)
- Secret rotation procedure: [docs/runbooks/secret-rotation.md](../../docs/runbooks/secret-rotation.md)
- ADR: [docs/decisions/004-infisical-for-secrets.md](../../docs/decisions/004-infisical-for-secrets.md)

## Subdirectories

| Directory | Description |
|---|---|
| [operator/](./operator/) | Infisical Operator Helm chart planning |
| [sync/](./sync/) | InfisicalSecret CRD planning per namespace |
