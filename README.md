# jAIMSnet

> <!-- LOGO PLACEHOLDER: Add jAIMSnet logo here -->
>
> **Open-source AI Management Systems infrastructure — ISO/IEC 42001 aligned**
> 
> **j** + **AIMS** (AI Management Systems) + **net** — Purpose-built for enterprise AI governance.

## Project Overview

jAIMSnet is an AI management systems platform integrating multiple services for AI infrastructure management across ♾️ WeOwnNet 🌐 ecosystem.

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Last Updated** | 2026-03-07 |
| **Cluster** | jaimsnet-cluster · DigitalOcean DOKS · ATL1 · K8s 1.34.1 |
| **ISO Reference** | [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) AI Management Systems |

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Architecture](#architecture)
- [Platform Status](#platform-status)
- [Infrastructure](#infrastructure)
- [Domains](#domains)
- [Compliance Targets](#compliance-targets)
- [Directory Index](#directory-index)
- [Team](#team)
- [Quick Start](#quick-start)
- [Cost Breakdown](#cost-breakdown)
- [Links](#links)

---

## Repository Structure

Monorepo (`jaimsnet/jaimsnet`) with structured directories for:
- `docs/` (architecture, deployment guide, ADRs, runbooks)
- `cluster/` (namespace definitions, ClusterIssuer)
- `ingress/` (ingress-nginx, cert-manager)
- `secrets/infisical/` (operator + sync CRDs)
- `gateway/` (LiteLLM, Redis)
- `observability/` (Langfuse, Prometheus, Grafana, Loki, Alloy, Mimir, Kuma)
- `gpu/` (vLLM on MI300X)
- `iac/` (OpenTofu, Ansible)
- `gitops/` (ArgoCD, Watchtower)
- `security/` (Kyverno, Trivy, Falco, CrowdSec, kube-bench, Docker Bench)
- `compliance/` (NIST CSF, CIS Controls, ISO 27001, ISO 42001, CCM, FedRAMP)
- `testing/` (integration, load, chaos)
- `scripts/` (utility scripts)

## Architecture
```
Internet → DO Load Balancer (129.212.240.75)
  → ingress-nginx
    → litellm.jAIMS.app  → LiteLLM     (gateway/)
    → langfuse.jAIMS.app → Langfuse    (observability/)
    → cert-manager (auto-TLS via Let's Encrypt)

LiteLLM → Redis            (gateway/redis)
LiteLLM → Langfuse         (callback / traces)
LiteLLM → OpenRouter / vLLM (providers)
LiteLLM → PostgreSQL       (spend tracking)
Langfuse → PostgreSQL      (traces + evals)

Infisical Cloud → Infisical Operator → K8s Secrets → Pods

Uptime Kuma (separate Droplet) → monitors all endpoints (kuma.jAIMS.app)

[Phase 2] vLLM on MI300X GPU Droplet (VPC) → LiteLLM backend
[Phase 2] Prometheus + Grafana + Loki + Alloy + Mimir
[Phase 2] Kyverno + Cilium Network Policies
[Phase 3] ArgoCD, Watchtower, Kyverno, Trivy, CrowdSec, Falco, kube-bench,
          docker-bench, Gitleaks, Syft, Grype, Ansible, full CI pipelines
[Phase 4] AI automation agents, customer-facing platform, k6 load testing,
          Litmus chaos engineering
```

---

## Platform Status

| Component | Tool | Phase | Status |
|---|---|---|---|
| Ingress controller | ingress-nginx | Phase 1 🔴 | 🔄 In Progress |
| TLS automation | cert-manager + Let's Encrypt | Phase 1 🔴 | 🔄 In Progress |
| AI gateway | LiteLLM | Phase 1 🔴 | 🔄 In Progress |
| Response caching | Redis | Phase 1 🔴 | 🔄 In Progress |
| LLM observability | Langfuse | Phase 1 🔴 | 🔄 In Progress |
| Secret management | Infisical Operator | Phase 1 🔴 | 🔄 In Progress |
| Endpoint monitoring | Uptime Kuma | Phase 1 🔴 | 🔄 In Progress |
| Infrastructure as Code | OpenTofu | Phase 1 🔴 | 🔄 In Progress |
| Metrics + dashboards | Prometheus + Grafana | Phase 2 🟠 | 📋 Planned |
| Log aggregation | Loki + Alloy | Phase 2 🟠 | 📋 Planned |
| Long-term metrics | Mimir | Phase 2 🟠 | 📋 Planned |
| GPU inference | vLLM on AMD MI300X | Phase 2 🟠 | 📋 Planned |
| Policy engine | Kyverno | Phase 2 🟠 | 📋 Planned |
| Network policies | Cilium | Phase 2 🟠 | 📋 Planned |
| GitOps (K8s) | ArgoCD | Phase 3 🟡 | 📋 Planned |
| GitOps (Docker) | Watchtower | Phase 3 🟡 | 📋 Planned |
| Image scanning | Trivy Operator | Phase 3 🟡 | 📋 Planned |
| Runtime security | Falco | Phase 3 🟡 | 📋 Planned |
| IDS + WAF | CrowdSec | Phase 3 🟡 | 📋 Planned |
| K8s benchmarking | kube-bench | Phase 3 🟡 | 📋 Planned |
| Docker benchmarking | docker-bench | Phase 3 🟡 | 📋 Planned |
| Secret scanning (CI) | Gitleaks | Phase 3 🟡 | 📋 Planned |
| SBOM generation | Syft + Grype | Phase 3 🟡 | 📋 Planned |
| Droplet automation | Ansible | Phase 3 🟡 | 📋 Planned |
| AI agents | TBD | Phase 4 🟢 | 📋 Planned |
| Load testing | k6 / Locust | Phase 4 🟢 | 📋 Planned |
| Chaos engineering | Litmus / Chaos Mesh | Phase 4 🟢 | 📋 Planned |

---

## Infrastructure

| Resource | Spec | Cost (est.) | Status |
|---|---|---|---|
| DOKS Cluster | jaimsnet-cluster · ATL1 · K8s 1.34.1 · Premium AMD 2vCPU/8GiB · autoscale 1-2 | ~$24/mo | 🔄 In Progress |
| DigitalOcean Load Balancer | 129.212.240.75 · ATL1 | ~$12/mo | ✅ Done |
| Managed PostgreSQL | ATL1 · port 25060 · sslmode=require | ~$15/mo | ✅ Done |
| Uptime Kuma Droplet | Basic Droplet · Docker | ~$6/mo | 📋 Planned |
| GPU Droplet (Phase 2) | AMD MI300X · ROCm · Docker | TBD | 📋 Planned |

---

## Domains

| Domain | Service | Status |
|---|---|---|
| `litellm.jAIMS.app` | LiteLLM AI Gateway | 🔄 In Progress |
| `langfuse.jAIMS.app` | Langfuse LLM Observability | 🔄 In Progress |
| `kuma.jAIMS.app` | Uptime Kuma Endpoint Monitor | 📋 Planned |
| `*.jaims.app` | Wildcard (future services) | 📋 Planned |
| `jaims.network` | Main platform domain | 📋 Planned |

---

## Compliance Targets

| Framework | Standard | Phase | Status |
|---|---|---|---|
| ISO/IEC 42001:2023 | AI Management Systems | Phase 3 🟡 | 📋 Planned |
| ISO/IEC 27001:2022 | Information Security Management | Phase 3 🟡 | 📋 Planned |
| SOC 2 Type II | Trust Service Criteria | Phase 3 🟡 | 📋 Planned |
| NIST CSF 2.0 | Cybersecurity Framework | Phase 3 🟡 | 📋 Planned |
| CIS Controls v8 | Security Best Practices | Phase 3 🟡 | 📋 Planned |
| CIS Benchmarks | K8s, Docker, Linux | Phase 3 🟡 | 📋 Planned |
| CSA CCM v4 | Cloud Controls Matrix | Phase 3 🟡 | 📋 Planned |
| FedRAMP | US Federal Cloud Security | Phase 4 🟢 | 📋 Planned |

> See [`compliance/`](./compliance/) for detailed framework mappings and evidence strategy.

---

## Directory Index

| Directory | Purpose | Phase |
|---|---|---|
| [`.github/`](./.github/) | CI workflows, CODEOWNERS, PR template | Phase 3 🟡 |
| [`docs/`](./docs/) | Architecture, deployment guide, ADRs, runbooks | Phase 1 🔴 |
| [`cluster/`](./cluster/) | DOKS cluster specs, namespace planning, network policies | Phase 1 🔴 |
| [`ingress/`](./ingress/) | ingress-nginx + cert-manager (TLS automation) | Phase 1 🔴 |
| [`secrets/`](./secrets/) | Infisical Operator + secret sync per namespace | Phase 1 🔴 |
| [`gateway/`](./gateway/) | LiteLLM AI gateway + Redis caching | Phase 1 🔴 |
| [`observability/`](./observability/) | Langfuse (AI), Prometheus/Grafana/Loki (infra), Uptime Kuma | Phase 1–2 |
| [`gpu/`](./gpu/) | vLLM on AMD MI300X GPU Droplet | Phase 2 🟠 |
| [`iac/`](./iac/) | OpenTofu (IaC) + Ansible (Droplet automation) | Phase 1–3 |
| [`gitops/`](./gitops/) | ArgoCD (K8s GitOps) + Watchtower (Docker) | Phase 3 🟡 |
| [`security/`](./security/) | Kyverno, Trivy, Falco, CrowdSec, kube-bench, docker-bench | Phase 2–3 |
| [`compliance/`](./compliance/) | Frameworks, policies, evidence collection | Phase 3 🟡 |
| [`testing/`](./testing/) | Integration, load, and chaos testing | Phase 3–4 |
| [`scripts/`](./scripts/) | Utility scripts (secret generation, backup, rotation) | Phase 1 🔴 |

---

## Team

| Member | Role | Responsibilities |
|---|---|---|
| @RMN | Platform + LLM Infrastructure | Gateway architecture, LiteLLM config, Langfuse, compliance strategy |
| @SHD | DevOps | Cluster operations, ingress, secrets, CI/CD, security tooling, Ansible |
| @LDC | Platform + Agentic AI | OpenTofu IaC, vLLM GPU, ArgoCD, Watchtower, AI automation |
| @GTM | Stakeholder | Requirements, compliance targets, customer platform, FedRAMP |

---

## Quick Start

> **Prerequisites:** `kubectl`, `helm` (≥ 3.12), `doctl` (DigitalOcean CLI), `tofu` (OpenTofu)

```bash
# 1. Authenticate to the cluster
doctl kubernetes cluster kubeconfig save jaimsnet-cluster

# 2. Verify cluster context
kubectl config current-context
kubectl config use-context do-atl1-jaimsnet-cluster

# 3. Verify node pool
kubectl get nodes -o wide

# 4. Check all namespaces
kubectl get namespaces

# 5. Check running workloads
kubectl get pods -A
```

> For full deployment steps see [`docs/deployment-guide.md`](./docs/deployment-guide.md).
> For operational runbooks see [`docs/runbooks/`](./docs/runbooks/).

---

## Cost Breakdown

| Phase | Monthly Cost (est.) | Components |
|---|---|---|
| Phase 1 🔴 | ~$57/mo | DOKS (1 node) + LB + Managed PG + Kuma Droplet |
| Phase 2 🟠 | ~$112+/mo | Phase 1 + autoscale node + GPU Droplet |
| Phase 3 🟡 | ~$120+/mo | Phase 2 + additional tooling overhead |
| Phase 4 🟢 | TBD | Phase 3 + customer platform infrastructure |

> Costs are estimates based on DigitalOcean ATL1 region pricing. Subject to change.

---

## Links

| Resource | URL |
|---|---|
| Platform domain | [jaims.network](https://jaims.network) |
| GitHub Organization | [github.com/jAIMSnet](https://github.com/jAIMSnet) |
| ISO/IEC 42001:2023 | [iso.org/standard/81230.html](https://www.iso.org/standard/81230.html) |
| LiteLLM docs | [docs.litellm.ai](https://docs.litellm.ai) |
| Langfuse docs | [langfuse.com/docs](https://langfuse.com/docs) |
| Infisical docs | [infisical.com/docs](https://infisical.com/docs) |
| OpenTofu | [opentofu.org](https://opentofu.org) |
