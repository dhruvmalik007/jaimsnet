# Watchtower

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Watchtower automatically monitors Docker containers on jAIMSnet Droplets and updates them when new image versions are pushed to the container registry.

## Deployment

| Parameter | Value |
|---|---|
| Target | Docker Droplets (not DOKS) |
| Deployment method | Docker Compose via Ansible |
| Schedule | Daily at 03:00 UTC |
| Notification | Slack webhook (Phase 3) |

## Managed Containers

| Droplet | Containers Watched | Auto-update |
|---|---|---|
| `uptime-kuma` | `uptime-kuma`, `caddy` | ✅ Enabled |
| `gpu-inference` | `vllm-*` | ⬜ Manual (GPU images) |

## Configuration Notes

- Watchtower runs in **monitor-only** mode for GPU containers (large images, manual approval required)
- Standard containers use `--rolling-restart` to minimize downtime
- Image update notifications will be sent to Slack in Phase 3

## Related

- [argocd/README.md](../argocd/README.md) — GitOps for K8s workloads
- [iac/ansible/roles/README.md](../../iac/ansible/roles/README.md)
