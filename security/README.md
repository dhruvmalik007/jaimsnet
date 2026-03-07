# Security

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 (Kyverno) / Phase 3 🟡 (Full Stack) |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Defense-in-depth security stack for jAIMSnet covering admission control, runtime detection, vulnerability management, IDS/WAF, and CIS benchmarking.

## Security Tools

| Tool | Directory | Purpose | Phase | Status |
|---|---|---|---|---|
| Kyverno | [kyverno/](./kyverno/) | K8s admission policy enforcement | Phase 2 🟠 | 📋 Planned |
| Trivy Operator | [trivy/](./trivy/) | In-cluster CVE + config scanning | Phase 3 🟡 | 📋 Planned |
| Falco | [falco/](./falco/) | Runtime security monitoring | Phase 3 🟡 | 📋 Planned |
| CrowdSec | [crowdsec/](./crowdsec/) | IDS + WAF for ingress and Droplets | Phase 3 🟡 | 📋 Planned |
| kube-bench | [kube-bench/](./kube-bench/) | CIS Kubernetes Benchmark | Phase 3 🟡 | 📋 Planned |
| docker-bench | [docker-bench/](./docker-bench/) | CIS Docker Benchmark on Droplets | Phase 3 🟡 | 📋 Planned |

## Coverage

| Layer | Control | Tool |
|---|---|---|
| Admission | Policy enforcement | Kyverno |
| Images | CVE scanning | Trivy Operator, Grype |
| Runtime | Anomaly detection | Falco |
| Network | IDS / WAF | CrowdSec, Cilium |
| Config | CIS Benchmarks | kube-bench, docker-bench |
| Secrets | Leak detection | Gitleaks (CI) |
| Supply Chain | SBOM | Syft + Grype (CI) |

## Compliance

Security tools feed directly into compliance evidence — see [compliance/evidence/README.md](../compliance/evidence/README.md).
