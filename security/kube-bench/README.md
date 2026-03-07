# kube-bench

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

kube-bench runs the CIS Kubernetes Benchmark against the jAIMSnet DOKS cluster, identifying configuration weaknesses against the CIS security standard.

## Deployment

| Method | Details |
|---|---|
| Run mode | Kubernetes Job (periodic) |
| Benchmark | CIS Kubernetes Benchmark v1.8+ |
| Output | JSON → stored as compliance evidence |

## Benchmark Sections

| Section | Description | Phase |
|---|---|---|
| Control Plane Configuration | API server, scheduler, controller-manager | Phase 3 🟡 |
| etcd | etcd security configuration | Phase 3 🟡 |
| Control Plane Policies | Pod security, network policies | Phase 3 🟡 |
| Worker Nodes | Kubelet configuration | Phase 3 🟡 |
| Kubernetes Policies | RBAC, PSS, network policies | Phase 3 🟡 |

## CI Integration

kube-bench runs scheduled in CI (Phase 3). Results are exported as JSON evidence to `compliance/evidence/` (gitignored raw data, summaries in docs).

## Compliance Mapping

- CIS Benchmarks (Kubernetes)
- SOC 2 CC6.1 (Logical Access Controls)
- ISO 27001 Annex A 8.9 (Configuration Management)
- NIST CSF PR.IP-1

## Related

- [compliance/frameworks/cis-benchmarks/README.md](../../compliance/frameworks/cis-benchmarks/README.md)
- [docker-bench/README.md](../docker-bench/README.md)
