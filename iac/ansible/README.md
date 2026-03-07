# Ansible

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Ansible manages configuration and application deployment on DigitalOcean Docker Droplets (Uptime Kuma, GPU inference, AnythingLLM, etc.). Kubernetes resources are managed via Helm/ArgoCD, not Ansible.

## Structure

```
iac/ansible/
├── inventory/      ← Host inventory (production, staging)
├── playbooks/      ← Deployment and configuration playbooks
└── roles/          ← Reusable roles
```

## Scope

| Managed By | Tool |
|---|---|
| DOKS cluster + resources | OpenTofu + Helm |
| Docker Droplets (Uptime Kuma, GPU, WordPress) | Ansible |
| DigitalOcean infrastructure | OpenTofu |

## Related

- [inventory/README.md](./inventory/README.md)
- [playbooks/README.md](./playbooks/README.md)
- [roles/README.md](./roles/README.md)
