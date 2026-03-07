# Ansible Playbooks

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Playbooks for configuring and deploying applications on jAIMSnet Docker Droplets.

## Playbook Index

| Playbook | File | Purpose | Phase | Status |
|---|---|---|---|---|
| Docker Droplet Setup | `setup-docker-droplet.yml` | Bootstrap Docker + firewall + hardening | Phase 3 🟡 | ⬜ TODO |
| Deploy AnythingLLM | `deploy-anythingllm.yml` | Deploy AnythingLLM on Docker Droplet | Phase 3 🟡 | ⬜ TODO |
| Deploy Uptime Kuma | `deploy-uptime-kuma.yml` | Deploy Uptime Kuma + Caddy | Phase 3 🟡 | ⬜ TODO |
| Deploy WordPress | `deploy-wordpress.yml` | Deploy WordPress + Caddy | Phase 3 🟡 | ⬜ TODO |
| Harden Droplet | `harden-droplet.yml` | CIS Docker Benchmark hardening | Phase 3 🟡 | ⬜ TODO |

## Playbook Conventions

- All playbooks use roles from [../roles/](../roles/)
- Secrets are fetched via Infisical lookup plugin (no hardcoded values)
- Idempotent — safe to re-run
- Each playbook has a `--check` (dry-run) compatible mode
