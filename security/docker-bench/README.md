# Docker Bench for Security

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Docker Bench for Security runs the CIS Docker Benchmark against jAIMSnet Docker Droplets, checking host configuration, Docker daemon settings, and container security.

## Deployment

| Method | Details |
|---|---|
| Execution | Ansible playbook (runs on each Droplet) |
| Benchmark | CIS Docker Benchmark v1.6+ |
| Schedule | Monthly + on-demand via CI |
| Output | JSON → compliance evidence |

## Benchmark Sections

| Section | Description |
|---|---|
| Host Configuration | OS hardening, Docker group membership |
| Docker Daemon Configuration | TLS, logging, live restore |
| Docker Daemon Files | Permissions on config files |
| Container Images | Base image security |
| Container Runtime | Capabilities, namespaces, read-only FS |
| Docker Security Operations | Seccomp, AppArmor, SELinux |

## Target Droplets

| Droplet | Phase | Status |
|---|---|---|
| `uptime-kuma` | Phase 3 🟡 | ⬜ TODO |
| `gpu-inference` | Phase 3 🟡 | ⬜ TODO |

## Compliance Mapping

- CIS Benchmarks (Docker)
- SOC 2 CC6.1 (Logical and Physical Access Controls)
- ISO 27001 Annex A 8.9 (Configuration Management)
- NIST CSF PR.IP-1

## Related

- [compliance/frameworks/cis-benchmarks/README.md](../../compliance/frameworks/cis-benchmarks/README.md)
- [kube-bench/README.md](../kube-bench/README.md)
- [iac/ansible/playbooks/README.md](../../iac/ansible/playbooks/README.md)
