# Ansible Inventory

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Ansible inventory structure for jAIMSnet Docker Droplets.

## Inventory Structure (Planned)

```
inventory/
├── production/
│   ├── hosts.yml         ← Static host definitions
│   └── group_vars/
│       ├── all.yml       ← Variables for all hosts
│       ├── docker.yml    ← Docker host group vars
│       └── gpu.yml       ← GPU host group vars
└── staging/              ← Phase 3
    └── hosts.yml
```

## Host Groups (Planned)

| Group | Hosts | Purpose |
|---|---|---|
| `docker` | `uptime-kuma`, `wordpress` | General Docker hosts |
| `gpu` | `gpu-inference` | AMD MI300X GPU Droplet |
| `monitoring` | `uptime-kuma` | Monitoring hosts |

## Variable Conventions

- Secrets are NOT stored in inventory files — fetched from Infisical via lookup plugin
- Host IPs are sourced from OpenTofu outputs
- SSH keys are managed via DigitalOcean project SSH key registry
