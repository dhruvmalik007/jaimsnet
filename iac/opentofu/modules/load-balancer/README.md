# Module: load-balancer

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | ✅ Done |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

OpenTofu module for the DigitalOcean managed Load Balancer that serves as the external entry point for all jAIMSnet ingress traffic.

## Resources Managed

| Resource | Type | Description |
|---|---|---|
| Load Balancer | `digitalocean_loadbalancer` | Managed LB |

## Current Production Config

| Parameter | Value |
|---|---|
| IP | `129.212.240.75` |
| Region | `atl1` |
| Type | DigitalOcean Managed LB |
| Backend | ingress-nginx NodePort |
| HTTP → HTTPS redirect | Enabled |
| Forwarding: HTTP 80 | → NodePort (ingress-nginx) |
| Forwarding: HTTPS 443 | → NodePort (ingress-nginx) |

## Notes

- The LB IP `129.212.240.75` is reserved and used in DNS A records
- TLS termination is handled by ingress-nginx + cert-manager (not at the LB)
- The LB is created by the DOKS ingress-nginx Helm chart annotation (`service.beta.kubernetes.io/do-loadbalancer-*`) — OpenTofu module may reference the existing LB rather than create a new one

## Planned Inputs

| Variable | Type | Description |
|---|---|---|
| `name` | `string` | LB name |
| `region` | `string` | DigitalOcean region |
| `vpc_uuid` | `string` | VPC attachment |

## Planned Outputs

| Output | Description |
|---|---|
| `lb_ip` | Load balancer public IP |
| `lb_id` | Load balancer ID |
