# Secrets

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

All secrets for jAIMSnet are managed in Infisical Cloud Pro and synced to Kubernetes via the Infisical Operator. No secrets are committed to Git.

## Structure

| Directory | Description |
|---|---|
| [infisical/](./infisical/) | Infisical operator + sync CRD planning |
| [infisical/operator/](./infisical/operator/) | Infisical Operator Helm chart planning |
| [infisical/sync/](./infisical/sync/) | InfisicalSecret CRD per namespace |

## Security Policy

- Secrets are **never** committed to Git (enforced via .gitignore and Gitleaks CI)
- All secrets use Kubernetes Auth — no static tokens in cluster
- Rotation procedure: [docs/runbooks/secret-rotation.md](../docs/runbooks/secret-rotation.md)
- ADR: [docs/decisions/004-infisical-for-secrets.md](../docs/decisions/004-infisical-for-secrets.md)
