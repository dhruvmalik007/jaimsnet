# CrowdSec

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

CrowdSec provides collaborative threat intelligence, intrusion detection (IDS), and web application firewall (WAF) capabilities for jAIMSnet. It covers both Kubernetes ingress traffic and Docker Droplet services.

## Deployment Targets

| Target | Component | Phase | Status |
|---|---|---|---|
| DOKS ingress | CrowdSec ingress-nginx bouncer | Phase 3 🟡 | ⬜ TODO |
| Docker Droplets | CrowdSec agent + firewall bouncer | Phase 3 🟡 | ⬜ TODO |

## Helm Chart (K8s)

| Field | Value |
|---|---|
| Repository | `https://crowdsecurity.github.io/helm-charts` |
| Chart | `crowdsec/crowdsec` |
| Namespace | `security` |

## Detection Scenarios

| Scenario | Source | Action |
|---|---|---|
| Brute force / credential stuffing | HTTP logs | Block IP |
| SQL injection / XSS attempts | WAF mode | Block request |
| CVE exploitation attempts | Community blocklist | Block IP |
| Port scanning | Network | Block IP |
| Rate limit violations | API gateway logs | Throttle |

## Community Intelligence

CrowdSec participates in the crowd-sourced threat intelligence network — blocked IPs are shared (anonymized) with the community, and the community blocklist is consumed automatically.

## Compliance Mapping

- SOC 2 CC6.6 (Logical Access Controls — prevent unauthorized access)
- ISO 27001 Annex A 8.22 (Filtering of Web Services)
- NIST CSF DE.CM-1, PR.PT-4
