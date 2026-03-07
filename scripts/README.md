# Scripts

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 / Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Utility scripts for jAIMSnet operations. All scripts are idempotent and documented.

## Script Index

| Script | Purpose | Phase | Status | Notes |
|---|---|---|---|---|
| generate-secrets.sh | Scaffold Infisical secret paths | Phase 1 🔴 | ⬜ TODO | Replaced by Infisical UI / CLI |
| backup-pg.sh | Trigger manual PostgreSQL backup | Phase 1 🔴 | ⬜ TODO | Via DigitalOcean API |
| verify-cluster.sh | Validate cluster health post-deploy | Phase 1 🔴 | ⬜ TODO | kubectl health checks |
| rotate-api-keys.sh | Trigger Infisical secret rotation | Phase 3 🟡 | ⬜ TODO | Wraps Infisical CLI |

## Conventions

- Scripts must not contain secrets or API keys
- Use Infisical CLI or environment variables for sensitive values
- Each script includes usage instructions at the top
- Scripts are validated in CI with shellcheck (Phase 3)
