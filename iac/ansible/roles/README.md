# Ansible Roles

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Reusable Ansible roles for jAIMSnet Droplet configuration.

## Role Index

| Role | Purpose | Phase | Status |
|---|---|---|---|
| `common` | Base OS setup, users, SSH config, apt updates | Phase 3 🟡 | ⬜ TODO |
| `docker` | Docker CE install + daemon config + Compose plugin | Phase 3 🟡 | ⬜ TODO |
| `firewall` | UFW rules (or DigitalOcean Cloud Firewall via API) | Phase 3 🟡 | ⬜ TODO |
| `watchtower` | Watchtower Docker auto-update agent | Phase 3 🟡 | ⬜ TODO |
| `node-exporter` | Prometheus Node Exporter (metrics for Mimir) | Phase 3 🟡 | ⬜ TODO |

## Role Conventions

- Follow Ansible Galaxy role structure (`tasks/`, `handlers/`, `defaults/`, `templates/`, `files/`)
- All sensitive values use `{{ lookup('infisical', ...) }}` — never hardcoded
- Roles are idempotent
