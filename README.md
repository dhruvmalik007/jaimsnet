# jAIMSnet — AI Infrastructure Platform

> **jAIMS** (jAI Management System) is a self-hosted, production-grade AI gateway and observability platform built on Kubernetes. It provides unified model routing, rate-limiting, cost tracking, and end-to-end LLM observability for engineering teams running private and third-party AI workloads.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Components](#key-components)
- [Directory Structure](#directory-structure)
- [Quick Start](#quick-start)
- [Deployment Phases](#deployment-phases)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

jAIMSnet manages the complete lifecycle of AI model traffic — from the moment a request enters the cluster, through routing and caching, to observability and cost attribution. It is designed to be **operator-friendly**, **secret-safe**, and **incrementally deployable**.

| Goal | Solution |
|---|---|
| Unified AI gateway | [LiteLLM](https://litellm.ai) Proxy |
| LLM observability & tracing | [Langfuse](https://langfuse.com) |
| Secret management | [Infisical](https://infisical.com) Operator |
| TLS automation | [cert-manager](https://cert-manager.io) + Let's Encrypt |
| Ingress & routing | [ingress-nginx](https://kubernetes.github.io/ingress-nginx/) |
| Response caching | [Redis](https://redis.io) |
| Infrastructure as Code | [OpenTofu](https://opentofu.org) |
| Metrics & dashboards *(Phase 2)* | Prometheus + Grafana + Loki |
| GitOps *(Phase 3)* | ArgoCD |
| GPU inference *(Phase 2)* | vLLM on AMD MI300X |
| Security scanning *(Phase 3)* | Trivy, CrowdSec |

---

## Architecture

```
                        ┌─────────────────────────────────────────────────────┐
                        │                   DOKS Cluster                       │
                        │                                                       │
  Internet              │  ┌──────────────┐      ┌───────────────────────┐    │
  ─────────►  ingress   │  │  ingress-    │      │      cert-manager     │    │
             (443/80)   │  │  nginx       │      │  (Let's Encrypt TLS)  │    │
                        │  └──────┬───────┘      └───────────────────────┘    │
                        │         │                                             │
                        │   ┌─────▼──────────────────────────┐                │
                        │   │           litellm               │                │
                        │   │   AI Gateway / Proxy            │                │
                        │   │  - Model routing & aliases      │                │
                        │   │  - Rate limiting & budgets      │◄──── Redis     │
                        │   │  - Fallback chains              │    (caching)   │
                        │   │  - Cost tracking                │                │
                        │   └─────────────┬───────────────────┘                │
                        │                 │  callbacks / traces                 │
                        │   ┌─────────────▼───────────────────┐                │
                        │   │           langfuse              │                │
                        │   │   LLM Observability             │                │
                        │   │  - Request/response tracing     │                │
                        │   │  - Token usage & cost per user  │                │
                        │   │  - Prompt versioning & evals    │                │
                        │   └─────────────────────────────────┘                │
                        │                                                       │
                        │   ┌─────────────────────────────────┐                │
                        │   │           infisical             │                │
                        │   │   Secret Operator               │                │
                        │   │  - Syncs secrets from Infisical │                │
                        │   │    cloud → K8s Secrets          │                │
                        │   │  - No secrets committed to Git  │                │
                        │   └─────────────────────────────────┘                │
                        │                                                       │
                        │   ┌──────────────────────────────────────────────┐   │
                        │   │  Phase 2: monitoring/              Phase 2:  │   │
                        │   │  Prometheus · Grafana · Loki     GPU / vLLM  │   │
                        │   └──────────────────────────────────────────────┘   │
                        └─────────────────────────────────────────────────────┘

  External AI Providers (OpenAI, Anthropic, Gemini, …)  ◄── LiteLLM routes to
  Self-hosted vLLM on AMD MI300X (Phase 2)              ◄──   these backends
```

### Traffic Flow

1. **Client** sends an OpenAI-compatible request to `litellm.jAIMS.app`.
2. **ingress-nginx** terminates TLS (cert managed by cert-manager) and proxies to LiteLLM.
3. **LiteLLM** applies routing rules, checks the Redis cache, enforces budgets, and forwards to the appropriate upstream model provider.
4. **Langfuse** receives structured traces via LiteLLM callbacks and stores them for analysis.
5. **Infisical Operator** keeps all provider API keys and service credentials synced as Kubernetes Secrets — nothing secret ever touches Git.

---

## Key Components

### AI Gateway (`gateway/`)
LiteLLM Proxy is the core AI gateway. Exposes an OpenAI-compatible API that routes to multiple model providers (OpenAI, Anthropic, Google Gemini, self-hosted vLLM, etc.). Supports:
- Named model aliases (e.g., `fast`, `smart`, `code`)
- Fallback chains for reliability
- Redis-backed semantic and exact-match caching
- Per-key and per-user budget enforcement
- Native Langfuse integration for observability callbacks

Redis runs in the same namespace as the gateway, providing response caching to reduce latency and provider costs.

### Observability (`observability/`)
Langfuse is the full-stack LLM observability platform. Captures every request and response as a trace, with token counts, latency, cost estimates, and user attribution. Provides:
- Prompt management and versioning
- Evaluation pipelines
- Real-time dashboards

Phase 2 will add Prometheus, Grafana, and Loki for infrastructure-level metrics and log aggregation.

### Secrets (`secrets/`)
Infisical Kubernetes operator that synchronizes secrets from Infisical (cloud or self-hosted) into native Kubernetes Secrets. `InfisicalSecret` CRDs for each namespace (`gateway-secrets.yaml`, `observability-secrets.yaml`) live here. **No credentials are stored in this repository.**

### Ingress & TLS (`ingress/`)
ingress-nginx is the cluster ingress controller. All external HTTPS traffic enters through this controller. Routes:
- `litellm.jAIMS.app` → LiteLLM service
- `langfuse.jAIMS.app` → Langfuse service

cert-manager automates TLS certificate provisioning and renewal using Let's Encrypt. Configured with a `ClusterIssuer` that handles all namespaces.

### Infrastructure as Code (`iac/`)
OpenTofu configurations for provisioning cloud infrastructure (e.g., DOKS cluster, DNS records, firewall rules). OpenTofu is the open-source Terraform-compatible IaC tool used throughout this project.

---

## Directory Structure

```
jaimsnet/
├── README.md
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── deployment-guide.md
│   ├── runbooks/
│   └── decisions/
│
├── cluster/                           # Cluster-level configs
│   ├── namespaces.yaml
│   ├── cluster-issuer.yaml
│   └── README.md
│
├── ingress/                           # Ingress + TLS
│   ├── ingress-nginx-values.yaml
│   ├── cert-manager-values.yaml
│   └── README.md
│
├── secrets/                           # Infisical operator + CRDs
│   ├── operator-values.yaml
│   ├── gateway-secrets.yaml           # InfisicalSecret for gateway namespace
│   ├── observability-secrets.yaml     # InfisicalSecret for observability namespace
│   └── README.md
│
├── gateway/                           # LiteLLM + Redis (AI Gateway)
│   ├── litellm-values.yaml
│   ├── litellm-config.yaml            # Routing aliases, models, fallbacks
│   ├── redis-values.yaml
│   ├── ingress.yaml                   # litellm.jAIMS.app
│   └── README.md
│
├── observability/                     # All observability tools
│   ├── langfuse/
│   │   ├── values.yaml
│   │   ├── ingress.yaml               # langfuse.jAIMS.app
│   │   └── README.md
│   ├── prometheus/                    # Phase 2
│   │   └── README.md
│   ├── grafana/                       # Phase 2
│   │   └── README.md
│   ├── loki/                          # Phase 2
│   │   └── README.md
│   └── README.md
│
├── iac/                               # OpenTofu IaC
│   └── README.md
│
├── gpu/                               # Phase 2: vLLM on MI300X
│   └── README.md
│
├── gitops/                            # Phase 3: ArgoCD
│   └── README.md
│
├── security/                          # Phase 3: Trivy, CrowdSec
│   └── README.md
│
└── scripts/
    ├── generate-secrets.sh
    └── README.md
```

---

## Quick Start

> **Prerequisites:** `kubectl`, `helm` (≥ 3.12), `doctl` (for DOKS), `tofu` (OpenTofu), access to an Infisical project with secrets populated.

```bash
# 1. Authenticate to the cluster
doctl kubernetes cluster kubeconfig save <cluster-name>

# 2. Create namespaces
kubectl apply -f cluster/namespaces.yaml

# 3. Install cert-manager
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  -f ingress/cert-manager-values.yaml

# 4. Apply the ClusterIssuer
kubectl apply -f cluster/cluster-issuer.yaml

# 5. Install ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  -f ingress/ingress-nginx-values.yaml

# 6. Install Infisical operator and sync secrets
helm upgrade --install infisical-operator infisical/infisical-operator \
  --namespace infisical --create-namespace \
  -f secrets/operator-values.yaml
kubectl apply -f secrets/gateway-secrets.yaml
kubectl apply -f secrets/observability-secrets.yaml

# 7. Deploy Redis + LiteLLM (AI Gateway)
helm upgrade --install redis bitnami/redis \
  --namespace gateway --create-namespace \
  -f gateway/redis-values.yaml
helm upgrade --install litellm litellm/litellm \
  --namespace gateway \
  -f gateway/litellm-values.yaml
kubectl apply -f gateway/ingress.yaml

# 8. Deploy Langfuse
helm upgrade --install langfuse langfuse/langfuse \
  --namespace observability --create-namespace \
  -f observability/langfuse/values.yaml
kubectl apply -f observability/langfuse/ingress.yaml
```

For the full step-by-step guide, see [`docs/deployment-guide.md`](docs/deployment-guide.md).

---

## Deployment Phases

| Phase | Status | Components |
|-------|--------|-----------|
| **Phase 1 — Core AI Platform** | 🚧 In Progress | ingress-nginx, cert-manager, Infisical, Redis, LiteLLM, Langfuse |
| **Phase 2 — Observability & GPU** | 📋 Planned | Prometheus, Grafana, Loki, vLLM on MI300X |
| **Phase 3 — GitOps & Security** | 📋 Planned | ArgoCD, Trivy, CrowdSec |

---

## Contributing

1. All secrets must be stored in Infisical — never in Git.
2. Each component lives in a logical directory with a `README.md`.
3. Infrastructure is managed with OpenTofu (`iac/`) — never Terraform.
4. Significant architectural decisions are recorded as ADRs in `docs/decisions/`.
5. See [`docs/deployment-guide.md`](docs/deployment-guide.md) for the operational workflow.

---

## License

Private repository — all rights reserved.
