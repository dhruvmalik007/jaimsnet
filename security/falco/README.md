# Falco

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Falco provides runtime security monitoring for the jAIMSnet Kubernetes cluster. It detects anomalous behavior using kernel-level syscall inspection and Kubernetes audit logs.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://falcosecurity.github.io/charts` |
| Chart | `falcosecurity/falco` |
| Namespace | `security` |
| Release name | `falco` |

## Detection Scenarios

| Scenario | Rule Category | Severity |
|---|---|---|
| Shell spawned in container | Container runtime | High |
| Sensitive file read | Filesystem | High |
| Outbound connection to unexpected host | Network | Medium |
| Privileged container started | Container runtime | Critical |
| K8s secret accessed directly | K8s Audit | High |
| Cryptominer-like behavior | Syscall | Critical |

## Alert Routing (Planned)

| Channel | Phase | Status |
|---|---|---|
| Falcosidekick → Slack | Phase 3 🟡 | ⬜ TODO |
| Falcosidekick → Loki | Phase 3 🟡 | ⬜ TODO |
| Falcosidekick → PagerDuty | Phase 4 🟢 | 📋 Planned |

## Compliance Mapping

- SOC 2 CC7.2 (Intrusion Detection)
- ISO 27001 Annex A 8.16 (Monitoring Activities)
- NIST CSF DE.CM-1 (Network Monitoring)
