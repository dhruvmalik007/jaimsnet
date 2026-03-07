# Module: database

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for provisioning DigitalOcean Managed PostgreSQL clusters used by LiteLLM and Langfuse.

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| DB Cluster | `digitalocean_database_cluster` | Managed PostgreSQL |
| DB (LiteLLM) | `digitalocean_database_db` | LiteLLM database |
| DB (Langfuse) | `digitalocean_database_db` | Langfuse database |
| DB User | `digitalocean_database_user` | Per-service DB users |
| Firewall rules | `digitalocean_database_firewall` | Restrict to VPC + DOKS |

## Current Production Config

| Parameter | Value |
|---|---|
| Region | `atl1` |
| Engine | PostgreSQL 16 |
| Size | `db-s-1vcpu-1gb` (Phase 1) |
| Port | `25060` |
| SSL mode | `require` |
| Standby | 0 (Phase 1) → 1 (Phase 2) |

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `cluster_name` | `string` | DB cluster name |
| `region` | `string` | DigitalOcean region |
| `size` | `string` | DB size slug |
| `node_count` | `number` | Number of nodes (1 = no standby) |
| `vpc_uuid` | `string` | VPC attachment |

## Planned Outputs

| Output | Description |
|---|---|
| `host` | DB host (sensitive) |
| `port` | DB port |
| `litellm_connection_uri` | LiteLLM DB URI (sensitive) |
| `langfuse_connection_uri` | Langfuse DB URI (sensitive) |
