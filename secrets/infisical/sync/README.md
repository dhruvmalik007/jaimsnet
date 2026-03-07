# InfisicalSecret Sync Definitions

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Planning for `InfisicalSecret` CRD manifests that define how secrets are synced from Infisical Cloud to each Kubernetes namespace.

## Planned Sync Resources

| CRD Name | Namespace | Infisical Path | K8s Secret | Phase | Status |
|---|---|---|---|---|---|
| `litellm-infisical-secret` | `gateway` | `/gateway/litellm` | `litellm-secrets` | Phase 1 🔴 | ⬜ TODO |
| `langfuse-infisical-secret` | `observability` | `/observability/langfuse` | `langfuse-secrets` | Phase 1 🔴 | ⬜ TODO |

## InfisicalSecret Structure Notes

Each `InfisicalSecret` CRD specifies:
- **Authentication**: Kubernetes Auth via service account
- **Infisical project + environment**: `production`
- **Secret path**: Folder path in Infisical
- **Target secret**: Name and namespace of the resulting K8s `Secret`
- **Resync interval**: How often the operator re-fetches (default: 1m)

## Related

- [operator/README.md](../operator/README.md)
- [docs/runbooks/secret-rotation.md](../../../docs/runbooks/secret-rotation.md)
