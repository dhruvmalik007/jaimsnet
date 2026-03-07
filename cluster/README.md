# Cluster

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

DOKS Kubernetes cluster configuration for jAIMSnet — hosted on DigitalOcean Kubernetes Service (DOKS) in the ATL1 region, running Kubernetes 1.34.1.

## Infrastructure

| Resource | Spec | Status |
|---|---|---|
| Cluster | jaimsnet-cluster, DOKS ATL1, K8s 1.34.1 | 🔄 In Progress |
| Node Pool | Premium AMD, 2vCPU/8GiB, autoscale 1-2 | 🔄 In Progress |
| Load Balancer | 129.212.240.75, DigitalOcean managed LB | ✅ Done |

## Related Files

| File | Description |
|---|---|
| [namespaces.md](./namespaces.md) | Namespace planning and inventory |
| [network-policies.md](./network-policies.md) | Cilium network policy planning (Phase 2) |

## Provisioning

The cluster is provisioned via OpenTofu — see [iac/opentofu/modules/doks-cluster/README.md](../iac/opentofu/modules/doks-cluster/README.md).
