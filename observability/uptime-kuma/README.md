# Uptime Kuma

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Uptime Kuma provides external uptime monitoring and public status page for jAIMSnet services. It runs on a dedicated Docker Droplet (not in the DOKS cluster) to ensure independence from the monitored infrastructure.

## Deployment

| Parameter | Value |
|---|---|
| Host | Dedicated DigitalOcean Docker Droplet |
| Deployment method | Docker Compose (via Ansible) |
| Domain | `kuma.jAIMS.app` |
| TLS | Caddy reverse proxy (automatic HTTPS) |
| Data persistence | Docker volume |

## Monitored Endpoints

| Monitor | URL | Interval | Alert Channel |
|---|---|---|---|
| LiteLLM API | `https://litellm.jAIMS.app/health` | 1 min | TBD |
| Langfuse | `https://langfuse.jAIMS.app/api/public/health` | 1 min | TBD |
| PostgreSQL | TCP port 25060 | 2 min | TBD |
| DOKS API server | K8s API health endpoint | 2 min | TBD |

## Ansible Management

Uptime Kuma is deployed and managed via Ansible:
- Playbook: `iac/ansible/playbooks/deploy-uptime-kuma.yml` (Phase 3)
- Role: `iac/ansible/roles/docker/` (Phase 3)

## Related

- [docs/runbooks/incident-response.md](../../docs/runbooks/incident-response.md)
- [iac/ansible/playbooks/README.md](../../iac/ansible/playbooks/README.md)
