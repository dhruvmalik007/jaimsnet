# CI/CD Workflows

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | ⬜ TODO |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

CI pipeline definitions for validating, scanning, and deploying jAIMSnet infrastructure. All workflows are planned for Phase 3 implementation via GitHub Actions.

## Planned Workflows

| Workflow | File | Purpose | Phase | Status |
|---|---|---|---|---|
| Helm Lint | `helm-lint.yaml` | Validate Helm charts | Phase 3 🟡 | ⬜ TODO |
| Kubeconform | `kubeconform.yaml` | Validate K8s manifests | Phase 3 🟡 | ⬜ TODO |
| OpenTofu Validate | `tofu-validate.yaml` | Validate OpenTofu modules | Phase 3 🟡 | ⬜ TODO |
| Ansible Lint | `ansible-lint.yaml` | Validate Ansible playbooks | Phase 3 🟡 | ⬜ TODO |
| YAML Lint | `yamllint.yaml` | YAML syntax check | Phase 3 🟡 | ⬜ TODO |
| Gitleaks | `gitleaks.yaml` | Secret scanning | Phase 3 🟡 | ⬜ TODO |
| Trivy Scan | `trivy-scan.yaml` | Image vulnerability scanning | Phase 3 🟡 | ⬜ TODO |
| Syft + Grype | `syft-grype.yaml` | SBOM + dependency scan | Phase 3 🟡 | ⬜ TODO |
| Docker Build | `docker-build.yaml` | Build + push images | Phase 3 🟡 | ⬜ TODO |
| Integration Test | `integration-test.yaml` | Endpoint integration tests | Phase 3 🟡 | ⬜ TODO |

## Design Notes

- All workflows will use GitHub-managed runners (ubuntu-latest)
- Secrets will be sourced from GitHub Actions secrets (mirrored from Infisical)
- PR workflows run on `pull_request` events; deploy workflows on `push` to `main`
- Scan results will be uploaded to GitHub Security tab via SARIF
