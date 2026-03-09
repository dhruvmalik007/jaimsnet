# ADR-003: DOKS Over Self-Managed Kubernetes on Droplets

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @SHD |
| **Deciders** | @SHD, @RMN, @LDC |

## Context

jAIMSnet requires a Kubernetes environment to host LiteLLM, Langfuse, Infisical Operator, and supporting services. A choice was needed between DigitalOcean Kubernetes Service (DOKS) and self-managed K8s on raw Droplets.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **DOKS** | Managed control plane, auto-upgrade, integrated LB, DO registry, no etcd management | Less control over control plane config, costs more than bare Droplets |
| Self-managed (kubeadm) | Full control, cheaper at scale | High operational burden: etcd backups, upgrades, HA |
| Self-managed (k3s) | Lightweight, simple | Not battle-tested for production at scale, less DO LB integration |

## Decision

Use **DigitalOcean Kubernetes Service (DOKS)** for the jAIMSnet cluster.

## Configuration

| Parameter | Value |
|---|---|
| Cluster name | jaimsnet-cluster |
| Region | ATL1 |
| Kubernetes version | 1.34.1 |
| Node size | Premium AMD 2vCPU/8GiB (s-2vcpu-8gb-amd) |
| Autoscale | 1-2 nodes |
| Load Balancer | DigitalOcean managed (129.212.240.75) |

## Consequences

### Positive
- Zero control plane management overhead
- DigitalOcean handles etcd, API server HA, and K8s upgrades
- Native DO LB integration via ingress-nginx annotations
- kube-bench partial compliance (some control plane benchmarks N/A for managed K8s)

### Negative / Trade-offs
- Some CIS Kubernetes Benchmark controls not applicable (managed control plane)
- Less flexibility for advanced K8s API server flags

## References
- [iac/opentofu/modules/doks-cluster/README.md](../../iac/opentofu/modules/doks-cluster/README.md)
- [DigitalOcean DOKS](https://docs.digitalocean.com/products/kubernetes/)
