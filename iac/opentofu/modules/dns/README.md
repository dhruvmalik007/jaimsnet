# Module: dns

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for managing DNS records for `jaims.app` and `jaims.network` via DigitalOcean DNS.

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| Domain | `digitalocean_domain` | DNS zone |
| A records | `digitalocean_record` | Service endpoints |
| CNAME records | `digitalocean_record` | Aliases |

## Planned DNS Records

| Record | Type | Value | Purpose |
|---|---|---|---|
| `litellm.jAIMS.app` | A | `129.212.240.75` | LiteLLM gateway |
| `langfuse.jAIMS.app` | A | `129.212.240.75` | Langfuse UI |
| `kuma.jAIMS.app` | A | `<uptime-kuma-droplet-ip>` | Uptime Kuma |
| `*.jaims.app` | A | `129.212.240.75` | Wildcard (Phase 2) |
| `jaims.network` | A | TBD | Secondary domain |

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `domain` | `string` | Root domain name |
| `lb_ip` | `string` | Load balancer IP for A records |
| `records` | `list(object)` | List of DNS record definitions |
