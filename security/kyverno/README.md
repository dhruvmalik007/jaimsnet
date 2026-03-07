# Kyverno

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Kyverno is the Kubernetes-native policy engine for jAIMSnet. It enforces security and governance policies at admission time without requiring an external policy language.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://kyverno.github.io/kyverno/` |
| Chart | `kyverno/kyverno` |
| Namespace | `security` |
| Release name | `kyverno` |

## Policy Categories

| Category | Policies | Phase | Status |
|---|---|---|---|
| Pod Security | require-non-root, disallow-privileged | Phase 2 🟠 | ⬜ TODO |
| Resource Management | require-resource-limits, require-labels | Phase 2 🟠 | ⬜ TODO |
| Supply Chain | restrict-image-registries | Phase 2 🟠 | ⬜ TODO |

## Related

- [policies/README.md](./policies/README.md)
- [ADR — TBD]
