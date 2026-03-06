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

### LiteLLM (`litellm/`)
The core AI gateway. Exposes an OpenAI-compatible API that routes to multiple model providers (OpenAI, Anthropic, Google Gemini, self-hosted vLLM, etc.). Supports:
- Named model aliases (e.g., `fast`, `smart`, `code`)
- Fallback chains for reliability
- Redis-backed semantic and exact-match caching
- Per-key and per-user budget enforcement
- Native Langfuse integration for observability callbacks

### Langfuse (`langfuse/`)
Full-stack LLM observability platform. Captures every request and response as a trace, with token counts, latency, cost estimates, and user attribution. Provides:
- Prompt management and versioning
- Evaluation pipelines
- Real-time dashboards

### Infisical (`infisical/`)
Kubernetes operator that synchronizes secrets from Infisical (cloud or self-hosted) into native Kubernetes Secrets. Each namespace that needs secrets has a corresponding `InfisicalSecret` CRD in `infisical/infisical-secrets/`. **No credentials are stored in this repository.**

### Redis (`redis/`)
In-cluster Redis instance used by LiteLLM for response caching. Reduces latency and provider costs for repeated or semantically similar queries.

### ingress-nginx (`ingress-nginx/`)
The cluster ingress controller. All external HTTPS traffic enters through this controller. Routes:
- `litellm.jAIMS.app` → LiteLLM service
- `langfuse.jAIMS.app` → Langfuse service

### cert-manager (`cert-manager/`)
Automates TLS certificate provisioning and renewal using Let's Encrypt. Configured with a `ClusterIssuer` that handles all namespaces.

---

## Directory Structure

```
jaimsnet/
├── README.md                          # This file
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── deployment-guide.md
│   ├── runbooks/
│   │   ├── litellm-operations.md
│   │   ├── langfuse-operations.md
│   │   └── disaster-recovery.md
│   └── decisions/
│       ├── 001-litellm-over-alternatives.md
│       ├── 002-langfuse-over-phoenix.md
│       ├── 003-doks-over-droplet.md
│       └── 004-infisical-for-secrets.md
│
├── cluster/                           # Cluster-level configs
│   ├── namespaces.yaml
│   ├── cluster-issuer.yaml
│   └── README.md
│
├── ingress-nginx/
│   ├── values.yaml
│   └── README.md
│
├── cert-manager/
│   ├── values.yaml
│   └── README.md
│
├── infisical/
│   ├── values.yaml
│   ├── infisical-secrets/
│   │   ├── litellm-secrets.yaml
│   │   ├── langfuse-secrets.yaml
│   │   └── redis-secrets.yaml
│   └── README.md
│
├── redis/
│   ├── values.yaml
│   └── README.md
│
├── litellm/
│   ├── values.yaml
│   ├── config.yaml
│   ├── ingress.yaml
│   └── README.md
│
├── langfuse/
│   ├── values.yaml
│   ├── ingress.yaml
│   └── README.md
│
├── monitoring/                        # Phase 2
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── README.md
│
├── gitops/                            # Phase 3
│   └── README.md
│
├── security/                          # Phase 3
│   └── README.md
│
├── gpu/                               # Phase 2
│   ├── docker-compose.vllm.yaml
│   ├── gpu-health.sh
│   └── README.md
│
└── scripts/
    ├── generate-secrets.sh
    ├── backup.sh
    └── README.md
```

---

## Quick Start

> **Prerequisites:** `kubectl`, `helm` (≥ 3.12), `doctl` (for DOKS), access to an Infisical project with secrets populated.

```bash
# 1. Authenticate to the cluster
doctl kubernetes cluster kubeconfig save <cluster-name>

# 2. Create namespaces
kubectl apply -f cluster/namespaces.yaml

# 3. Install cert-manager
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  -f cert-manager/values.yaml

# 4. Apply the ClusterIssuer
kubectl apply -f cluster/cluster-issuer.yaml

# 5. Install ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  -f ingress-nginx/values.yaml

# 6. Install Infisical operator and sync secrets
helm upgrade --install infisical-operator infisical/infisical-operator \
  --namespace infisical --create-namespace \
  -f infisical/values.yaml
kubectl apply -f infisical/infisical-secrets/

# 7. Install Redis
helm upgrade --install redis bitnami/redis \
  --namespace redis --create-namespace \
  -f redis/values.yaml

# 8. Deploy LiteLLM
helm upgrade --install litellm litellm/litellm \
  --namespace litellm --create-namespace \
  -f litellm/values.yaml
kubectl apply -f litellm/ingress.yaml

# 9. Deploy Langfuse
helm upgrade --install langfuse langfuse/langfuse \
  --namespace langfuse --create-namespace \
  -f langfuse/values.yaml
kubectl apply -f langfuse/ingress.yaml
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
2. Each component lives in its own top-level directory with a `README.md`.
3. Significant architectural decisions are recorded as ADRs in `docs/decisions/`.
4. See [`docs/deployment-guide.md`](docs/deployment-guide.md) for the operational workflow.

---

## License

Private repository — all rights reserved.
