# Observability

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 (Langfuse) / Phase 2 🟠 (Full Stack) |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Three-layer observability architecture for jAIMSnet: AI-specific tracing (Phase 1), infrastructure metrics and logs (Phase 2), and external uptime monitoring (Phase 1).

## Architecture

| Layer | Component | Purpose | Phase | Status |
|---|---|---|---|---|
| AI Observability | Langfuse | LLM trace logging, cost tracking, evals | Phase 1 🔴 | 🔄 In Progress |
| Infrastructure Metrics | Prometheus + Grafana + Mimir | K8s and app metrics, dashboards, long-term storage | Phase 2 🟠 | 📋 Planned |
| Log Aggregation | Loki + Alloy | Centralized log collection and querying | Phase 2 🟠 | 📋 Planned |
| External Uptime | Uptime Kuma | Public status page, external health checks | Phase 1 🔴 | 🔄 In Progress |

## Components

| Directory | Component | Description |
|---|---|---|
| [langfuse/](./langfuse/) | Langfuse | AI observability platform |
| [prometheus/](./prometheus/) | Prometheus | Metrics collection |
| [grafana/](./grafana/) | Grafana | Dashboards and alerting |
| [loki/](./loki/) | Loki | Log aggregation |
| [alloy/](./alloy/) | Grafana Alloy | Unified telemetry collector |
| [mimir/](./mimir/) | Grafana Mimir | Long-term metrics storage |
| [uptime-kuma/](./uptime-kuma/) | Uptime Kuma | External uptime monitoring |

## Related

- [ADR-002](../docs/decisions/002-langfuse-over-phoenix.md) — Langfuse decision
