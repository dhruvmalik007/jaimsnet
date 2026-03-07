# Module: droplet

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for provisioning DigitalOcean Droplets used as Docker hosts (Uptime Kuma, GPU inference, etc.).

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| Droplet | `digitalocean_droplet` | VM instance |
| Firewall | `digitalocean_firewall` | Inbound/outbound rules |
| Volume (optional) | `digitalocean_volume` | Persistent block storage |

## Planned Droplets

| Name | Size | Purpose | Phase |
|---|---|---|---|
| `uptime-kuma` | `s-1vcpu-1gb` | Uptime Kuma + Caddy | Phase 1 🔴 |
| `gpu-inference` | GPU Droplet (MI300X) | vLLM inference | Phase 2 🟠 |

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `name` | `string` | Droplet name |
| `region` | `string` | DigitalOcean region |
| `size` | `string` | Droplet size slug |
| `image` | `string` | OS image (e.g., `ubuntu-22-04-x64`) |
| `ssh_key_ids` | `list(string)` | SSH key IDs for access |
| `vpc_uuid` | `string` | VPC attachment |
| `tags` | `list(string)` | Resource tags |
| `user_data` | `string` | Cloud-init script (optional) |

## Planned Outputs

| Output | Description |
|---|---|
| `droplet_id` | Droplet ID |
| `ipv4_address` | Public IPv4 address |
| `ipv4_address_private` | Private VPC IPv4 |
