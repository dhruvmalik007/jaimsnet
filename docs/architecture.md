# jAIMSnet Architecture

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

System architecture overview for jAIMSnet — AI infrastructure management platform built on DigitalOcean.

## Platform Summary

| Component | Technology | Host | Status |
|---|---|---|---|
| LLM Gateway | LiteLLM | DOKS - gateway namespace | 🔄 In Progress |
| AI Observability | Langfuse | DOKS - observability namespace | 🔄 In Progress |
| Cache | Redis | DOKS - gateway namespace | 🔄 In Progress |
| Secrets | Infisical Cloud Pro + K8s Operator | DOKS - infisical namespace | 🔄 In Progress |
| Ingress | ingress-nginx + cert-manager | DOKS - ingress-nginx / cert-manager | 🔄 In Progress |
| GPU Inference | vLLM on AMD MI300X | GPU Droplet (Docker) | 📋 Planned Phase 2 |
| Metrics Stack | Prometheus + Grafana + Mimir + Loki + Alloy | DOKS - monitoring namespace | 📋 Planned Phase 2 |
| Uptime Monitoring | Uptime Kuma | Docker Droplet | 🔄 In Progress |
| IaC | OpenTofu | Managed locally | 🔄 In Progress |
| GitOps | ArgoCD | DOKS - argocd namespace | 📋 Planned Phase 3 |

## Infrastructure

| Resource | Value |
|---|---|
| Cloud Provider | DigitalOcean |
| Kubernetes | DOKS jaimsnet-cluster, ATL1, K8s 1.34.1 |
| Node Pool | Premium AMD, 2vCPU/8GiB, autoscale 1-2 |
| Load Balancer IP | 129.212.240.75 |
| Database | Managed PostgreSQL, ATL1, port 25060, sslmode=require |
| Domains | litellm.jAIMS.app, langfuse.jAIMS.app, kuma.jAIMS.app |

## Phase Roadmap

| Phase | Focus | Status |
|---|---|---|
| Phase 1 🔴 | LiteLLM + Langfuse + Redis + Infisical + Uptime Kuma + OpenTofu | 🔄 In Progress |
| Phase 2 🟠 | Prometheus + Grafana + Loki + Alloy + Mimir + vLLM MI300X + Kyverno + Cilium | 📋 Planned |
| Phase 3 🟡 | ArgoCD + Watchtower + Trivy + CrowdSec + Falco + kube-bench + Gitleaks + Syft + Grype + Ansible + CI | 📋 Planned |
| Phase 4 🟢 | AI automation agents, customer platform, k6 load testing, Litmus chaos engineering | 📋 Planned |

## Team

| Handle | Role |
|---|---|
| @RMN | Platform Lead + LLM Infrastructure |
| @GTM | Stakeholder |
| @SHD | DevOps |
| @LDC | Platform + Agentic AI |
