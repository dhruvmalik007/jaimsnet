# Production Environment

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

Root OpenTofu module for the `production` environment. Composes all infrastructure modules for the jAIMSnet production deployment on DigitalOcean.

## Infrastructure Overview

| Resource | Module | Region | Status |
|---|---|---|---|
| DOKS Cluster (`jaimsnet-cluster`) | `doks-cluster` | ATL1 | 🔄 In Progress |
| Node Pool (Premium AMD 2vCPU/8GiB) | `doks-cluster` | ATL1 | 🔄 In Progress |
| PostgreSQL (managed, port 25060) | `database` | ATL1 | 🔄 In Progress |
| Load Balancer (129.212.240.75) | `load-balancer` | ATL1 | ✅ Done |
| VPC | `vpc` | ATL1 | 🔄 In Progress |
| DNS (jaims.app, jaims.network) | `dns` | Global | 🔄 In Progress |
| Uptime Kuma Droplet | `droplet` | ATL1 | 📋 Planned |
| GPU Droplet (MI300X) | `droplet` | ATL1 | 📋 Planned (Phase 2) |

## Variable Planning

| Variable | Description | Example |
|---|---|---|
| `do_region` | DigitalOcean region | `atl1` |
| `cluster_name` | DOKS cluster name | `jaimsnet-cluster` |
| `k8s_version` | Kubernetes version | `1.34.1-do.0` |
| `node_size` | Node pool size | `s-2vcpu-8gb-amd` |
| `node_min_count` | Min autoscale nodes | `1` |
| `node_max_count` | Max autoscale nodes | `2` |

> **Note:** Variable values are stored in `terraform.tfvars` (gitignored). Use `terraform.tfvars.example` as template.

## Related

- [../../modules/README.md](../../modules/README.md)
