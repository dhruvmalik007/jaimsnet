# Grafana Mimir

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Grafana Mimir provides long-term metrics storage for jAIMSnet, replacing ephemeral Prometheus storage with horizontally scalable, multi-tenant time-series storage backed by DigitalOcean Spaces (S3-compatible).

## Helm Chart

| Field | Value |
|---|---|
| Repository | `https://grafana.github.io/helm-charts` |
| Chart | `grafana/mimir-distributed` |
| Namespace | `monitoring` |
| Release name | `mimir` |

## Configuration Planning

| Parameter | Value | Notes |
|---|---|---|
| Deployment mode | Monolithic (Phase 2) | Simplified single-process for initial deployment |
| Object storage | DigitalOcean Spaces | S3-compatible backend |
| Retention | 90 days | Initial retention policy |
| Replication factor | `1` (Phase 2) → `3` (Phase 3) | HA in Phase 3 |

## Data Sources

| Metric Source | Collector | Notes |
|---|---|---|
| Kubernetes infra | Alloy DaemonSet | Node, pod, container metrics |
| LiteLLM | Alloy + ServiceMonitor | Request rate, latency, cost |
| Langfuse | Prometheus scrape | Trace counts, error rates |
| GPU metrics | Alloy + ROCm exporter | VRAM usage, GPU utilization |

## Related

- [alloy/README.md](../alloy/README.md)
- [grafana/README.md](../grafana/README.md)
