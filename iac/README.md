# Infrastructure as Code

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 (OpenTofu) / Phase 3 🟡 (Ansible) |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

Infrastructure as Code for jAIMSnet — OpenTofu manages DigitalOcean cloud resources, and Ansible configures Docker Droplets.

## Components

| Directory | Tool | Scope | Phase | Status |
|---|---|---|---|---|
| [opentofu/](./opentofu/) | OpenTofu | DOKS cluster, DBs, Droplets, DNS, VPC, LB | Phase 1 🔴 | 🔄 In Progress |
| [ansible/](./ansible/) | Ansible | Docker Droplet config, app deployment | Phase 3 🟡 | 📋 Planned |

## Tool Responsibilities

| Resource | Tool |
|---|---|
| DOKS cluster + node pools | OpenTofu |
| DigitalOcean managed PostgreSQL | OpenTofu |
| VPC, DNS, Load Balancer | OpenTofu |
| Docker Droplets (provisioning) | OpenTofu |
| Docker Droplets (configuration) | Ansible |
| Kubernetes resources | Helm + ArgoCD |
