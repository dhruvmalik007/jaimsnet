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

| Variable | Type | Required | Default | Description |
|---|---|---|---|---|
| `domain` | `string` | ✅ Yes | — | Root domain name (e.g., `jaims.app`) |
| `manage_domain` | `bool` | No | `true` | `true` = Terraform creates/owns the zone. `false` = references existing zone (read-only). Use `tofu import` to migrate an existing zone. |
| `lb_ip` | `string` | No | `""` | Load balancer IP used for A records when value is `""` or `"use_lb_ip"` |
| `records` | `list(object)` | No | `[]` | List of DNS record definitions (`name`, `type`, `value`) |
| `record_ttl` | `number` | No | `300` | TTL in seconds for A/CNAME records |

## Outputs

| Output | Description |
|---|---|
| `domain_name` | The domain name managed or referenced by this module |
| `domain_urn` | URN of the domain zone (only when `manage_domain = true`) |
| `manage_domain` | Echoes whether this module is managing (owning) the DNS zone |
| `routing_records` | List of created A/CNAME record FQDNs |

