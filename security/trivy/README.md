# Trivy Operator

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Trivy Operator provides continuous in-cluster vulnerability scanning of container images and Kubernetes configuration. It generates `VulnerabilityReport` and `ConfigAuditReport` CRDs for each workload.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://aquasecurity.github.io/helm-charts/` |
| Chart | `aquasecurity/trivy-operator` |
| Namespace | `security` |
| Release name | `trivy-operator` |

## Scan Types

| Scan Type | CRD | Description | Phase |
|---|---|---|---|
| Vulnerability | `VulnerabilityReport` | CVEs in container images | Phase 3 🟡 |
| Config Audit | `ConfigAuditReport` | K8s security misconfigs | Phase 3 🟡 |
| RBAC Assessment | `RbacAssessmentReport` | RBAC overprivilege detection | Phase 3 🟡 |
| SBOM | `SbomReport` | Software bill of materials | Phase 3 🟡 |

## CI Integration

Trivy also runs in CI (GitHub Actions) via `trivy-scan.yaml` workflow — see [.github/workflows/README.md](../../.github/workflows/README.md).

## Compliance Mapping

Trivy findings feed into:
- SOC 2 CC6.8 (Vulnerability Management)
- ISO 27001 Annex A 8.8 (Technical Vulnerability Management)
- CIS Controls v8 Control 7 (Vulnerability Management)
