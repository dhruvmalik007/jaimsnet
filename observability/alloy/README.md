# Grafana Alloy

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Grafana Alloy (successor to Promtail and Grafana Agent) is the unified telemetry collector for jAIMSnet. It collects logs, metrics, and traces and ships them to Loki, Mimir, and Tempo.

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://grafana.github.io/helm-charts` |
| Chart | `grafana/alloy` |
| Namespace | `monitoring` |
| Release name | `alloy` |

## Planned Data Flows

| Source | Signal | Destination |
|---|---|---|
| All pod logs | Logs | Loki |
| Node metrics | Metrics | Mimir |
| Kubernetes metrics | Metrics | Mimir |
| LiteLLM metrics | Metrics | Mimir |
| Langfuse traces | Traces | Tempo (Phase 3) |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| `alloy.configMap.content` | Alloy River config | TBD in Phase 2 |
| `controller.type` | `daemonset` | One per node for log collection |
| `serviceMonitor.enabled` | `true` | Alloy self-monitoring |

## Related

- [mimir/README.md](../mimir/README.md)
- [prometheus/README.md](../prometheus/README.md)
- [loki/README.md](../loki/README.md)
