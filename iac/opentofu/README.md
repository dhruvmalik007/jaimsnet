# OpenTofu

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 (partial) |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu manages all DigitalOcean infrastructure for jAIMSnet — DOKS cluster, Droplets, managed databases, VPCs, DNS, and load balancers.

## Structure

```
iac/opentofu/
├── environments/
│   └── production/     ← Production environment root module
└── modules/
    ├── doks-cluster/   ← DOKS Kubernetes cluster
    ├── droplet/        ← DigitalOcean Droplets
    ├── database/       ← Managed PostgreSQL
    ├── dns/            ← DNS records
    ├── vpc/            ← Virtual Private Cloud
    └── load-balancer/  ← Load balancer
```

## Module Index

| Module | Purpose | Phase | Status |
|---|---|---|---|
| `doks-cluster` | DOKS Kubernetes cluster | Phase 1 🔴 | 🔄 In Progress |
| `droplet` | DigitalOcean Droplets (Uptime Kuma, GPU) | Phase 1 🔴 | 🔄 In Progress |
| `database` | Managed PostgreSQL (ATL1) | Phase 1 🔴 | 🔄 In Progress |
| `dns` | DNS records for jaims.app + jaims.network | Phase 1 🔴 | 🔄 In Progress |
| `vpc` | VPC for cluster + droplet isolation | Phase 1 🔴 | 🔄 In Progress |
| `load-balancer` | DigitalOcean LB (129.212.240.75) | Phase 1 🔴 | ✅ Done |

## Backend & State

| Parameter | Value |
|---|---|
| State backend | DigitalOcean Spaces (S3-compatible) |
| State file | `jaimsnet.tfstate` |
| Workspace | `production` |

## Related

- [environments/production/README.md](./environments/production/README.md)
- [modules/README.md](./modules/README.md)
- [ADR-003](../../docs/decisions/003-doks-over-droplet.md)
