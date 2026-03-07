# Module: vpc

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for provisioning a DigitalOcean Virtual Private Cloud (VPC) to network-isolate the DOKS cluster, Droplets, and managed database.

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| VPC | `digitalocean_vpc` | Private network |

## Current Production Config

| Parameter | Value |
|---|---|
| Name | `jaimsnet-vpc` |
| Region | `atl1` |
| IP range | `10.10.0.0/16` |

## Network Isolation Design

| Resource | VPC Attachment |
|---|---|
| DOKS cluster | ✅ Attached |
| PostgreSQL | ✅ Attached |
| Droplets | ✅ Attached |
| Load Balancer | Via DOKS annotation |

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `name` | `string` | VPC name |
| `region` | `string` | DigitalOcean region |
| `ip_range` | `string` | CIDR block |

## Planned Outputs

| Output | Description |
|---|---|
| `vpc_id` | VPC UUID |
| `vpc_urn` | VPC URN |
| `ip_range` | Allocated CIDR |
