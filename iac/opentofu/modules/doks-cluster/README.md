# Module: doks-cluster

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for provisioning a DigitalOcean Kubernetes Service (DOKS) cluster with a managed node pool.

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| Cluster | `digitalocean_kubernetes_cluster` | DOKS cluster |
| Node pool | `digitalocean_kubernetes_node_pool` | Autoscaling node pool |

## Current Production Config

| Parameter | Value |
|---|---|
| Cluster name | `jaimsnet-cluster` |
| Region | `atl1` |
| Kubernetes version | `1.34.1-do.0` |
| Node size | `s-2vcpu-8gb-amd` (Premium AMD) |
| Min nodes | `1` |
| Max nodes | `2` |
| Auto-upgrade | Enabled |
| Surge upgrade | Enabled |

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `cluster_name` | `string` | Name of the DOKS cluster |
| `region` | `string` | DigitalOcean region |
| `k8s_version` | `string` | Kubernetes version slug |
| `node_size` | `string` | Droplet size for nodes |
| `node_min_count` | `number` | Minimum autoscale count |
| `node_max_count` | `number` | Maximum autoscale count |
| `vpc_uuid` | `string` | VPC to attach cluster to |
| `tags` | `list(string)` | Resource tags |

## Planned Outputs

| Output | Description |
|---|---|
| `cluster_id` | DOKS cluster ID |
| `cluster_endpoint` | Kubernetes API server endpoint |
| `kubeconfig` | Kubeconfig (sensitive) |
