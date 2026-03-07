# CIS Benchmarks

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

CIS Benchmarks provide hardened configuration standards for specific technologies. jAIMSnet targets three benchmarks, all automated via tooling.

## Benchmark Coverage

| Benchmark | Version | Tool | Target | Phase | Status |
|---|---|---|---|---|---|
| CIS Kubernetes Benchmark | v1.8+ | kube-bench | DOKS cluster | Phase 3 🟡 | 📋 Planned |
| CIS Docker Benchmark | v1.6+ | docker-bench | GPU + Uptime Kuma Droplets | Phase 3 🟡 | 📋 Planned |
| CIS Linux (Ubuntu) Benchmark | v2.0+ | Ansible audit role | All Droplets | Phase 3 🟡 | 📋 Planned |

## Automation

| Benchmark | Trigger | Schedule | Evidence Output |
|---|---|---|---|
| kube-bench | K8s Job | Monthly | JSON → `compliance/evidence/` |
| docker-bench | Ansible playbook | Monthly | JSON → `compliance/evidence/` |
| Linux audit | Ansible playbook | Monthly | JSON → `compliance/evidence/` |

## Compliance Mapping

| Benchmark | SOC 2 | ISO 27001 | NIST CSF |
|---|---|---|---|
| CIS Kubernetes | CC6.1, CC7.1 | A.8.9, A.8.8 | PR.IP-1, PR.PT-4 |
| CIS Docker | CC6.1, CC7.1 | A.8.9 | PR.IP-1 |
| CIS Linux | CC6.1, CC7.1 | A.8.9 | PR.IP-1 |

## Related

- [security/kube-bench/README.md](../../../security/kube-bench/README.md)
- [security/docker-bench/README.md](../../../security/docker-bench/README.md)
