# iac/ — WeOwn AI Infrastructure as Code

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Product Tiers](#product-tiers)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Module Reference](#module-reference)
- [Environment Configuration](#environment-configuration)
- [State Management](#state-management)
- [Secrets Management](#secrets-management)
- [Deployment Guide](#deployment-guide)
- [Testing](#testing)
- [CI/CD — GitHub Actions](#cicd--github-actions)
- [Networking & Security](#networking--security)
- [Cost Matrix](#cost-matrix)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Related Projects](#related-projects)

---

## Overview

This directory contains the OpenTofu Infrastructure as Code (IaC)
implementation for the WeOwn AI platform. It provisions and manages
all cloud infrastructure required to deploy AnythingLLM-based AI
instances across two product tiers:

| Tier | Infrastructure | Target |
|------|---------------|--------|
| **WeOwn Lite AI** | Single DO Droplet + shared GPU | Cost-conscious customers |
| **WeOwn Pro AI** | DOKS Cluster + dedicated GPU + managed DB | Enterprise / compliance-required |

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| **FOSS First** | OpenTofu (MPL-2.0) — not Terraform (BSL) |
| **Declarative** | HCL defines desired state — OpenTofu converges |
| **Modular** | Reusable modules composed per environment |
| **Reproducible** | Any environment can be recreated from code |
| **Secure** | State encryption at rest, secrets via Infisical |
| **One-Command** | `weown-cli deploy` |

---

## Architecture

The architecture is divided into the **Core Shared Infrastructure** (jAIMS Gateway) and the **Compute Deployments** (Customer Droplets or k8s clusters).

### Core Shared Infrastructure (jAIMS AI Gateway)

The core infrastructure is centrally managed and provides shared AI routing, observability, and secrets management:

```text
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
```

### Edge Deployments (Customer Instances)

Customer-facing AI interfaces (like AnythingLLM) are deployed via the `weown-cli` droplet pipeline on an isolated, per-instance basis. These edge instances are pre-configured to connect directly to the shared Core Infrastructure:

```text
┌─────────────────────────────────────────────────────┐
│                  DigitalOcean ATL1                  │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │          Shared VPC: 10.10.20.0/24           │   │
│  │                                              │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │  Droplet: anythingllm-<ccc-id-name>    │  │   │
│  │  │  ┌──────────────┐  ┌───────────────┐   │  │   │
│  │  │  │  AnythingLLM │  │    Caddy      │   │  │   │
│  │  │  │  :3001       │  │  :80/:443     │   │  │   │
│  │  │  │              │  │  (HTTPS Proxy)│   │  │   │
│  │  │  └──────┬───────┘  └───────────────┘   │  │   │
│  │  └─────────┼──────────────────────────────┘  │   │
│  │            │                                 │   │
│  └────────────┼─────────────────────────────────┘   │
│               │ API Calls                           │
│               ▼                                     │
│     ┌────────────────────────────────────┐          │
│     │        jAIMS Core Gateway          │          │
│     │   (litellm.jAIMS.app + langfuse)   │          │
│     └────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

### Future Phases

- **[Phase 2]** vLLM on MI300X GPU Droplet (VPC) → LiteLLM backend
- **[Phase 2]** Prometheus + Grafana + Loki + Alloy + Mimir
- **[Phase 2]** Kyverno + Cilium Network Policies
- **[Phase 3]** ArgoCD, Watchtower, Kyverno, Trivy, CrowdSec, Falco, kube-bench, docker-bench, Gitleaks, Syft, Grype, Ansible, full CI pipelines
- **[Phase 4]** AI automation agents, customer-facing platform, k6 load testing, Litmus chaos engineering

---

## Tech Stack

| Category | Tool | License | Module | Phase |
|----------|------|---------|--------|-------|
| **IaC** | OpenTofu | MPL-2.0 | — | Phase 1 |
| **Compute** | DO Droplet | — | `droplet/` | Phase 1 |
| **Compute** | DO DOKS | — | `doks/` | Phase 1 |
| **Compute** | MI300X GPU | — | `gpu/` | Phase 2 |
| **Database** | PostgreSQL 18 | PostgreSQL | `database/` | Phase 1 |
| **AI** | AnythingLLM | MIT | `droplet/` / Helm | Phase 1 |
| **AI Gateway** | LiteLLM | MIT | Helm (gateway/) | Phase 1 |
| **AI Inference** | vLLM | Apache 2.0 | `gpu/` | Phase 2 |
| **Observability** | Langfuse | MIT | `observability/langfuse/` | Phase 1 |
| **Observability** | Uptime Kuma | MIT | `observability/uptime-kuma/` | Phase 1 |
| **Observability** | Grafana Alloy | Apache 2.0 | `observability/grafana-alloy/` | Phase 2 |
| **Observability** | Mimir | AGPL-3.0 | `observability/mimir/` | Phase 2 |
| **Observability** | Prometheus | Apache 2.0 | Helm | Phase 2 |
| **Observability** | Grafana | AGPL-3.0 | Helm | Phase 2 |
| **Observability** | Loki | AGPL-3.0 | Helm | Phase 2 |
| **Internal** | n8n | ⚠️ Sustainable Use | `internal-tools/n8n/` | Phase 1 |
| **Internal** | Vaultwarden | AGPL-3.0 | `internal-tools/vaultwarden/` | Phase 1 |
| **Collaboration** | Matomo | GPL-3.0 | `collaboration/matomo/` | Phase 3 |
| **Collaboration** | Nextcloud | AGPL-3.0 | `collaboration/nextcloud/` | Phase 3 |
| **Collaboration** | Stalwart | AGPL-3.0 | `collaboration/mail/stalwart/` | Phase 3 |
| **Collaboration** | Postal | MIT | `collaboration/mail/postal/` | Phase 3 |
| **GitOps** | ArgoCD | Apache 2.0 | `gitops/argocd/` | Phase 3 |
| **GitOps** | Watchtower | Apache 2.0 | `gitops/watchtower/` | Phase 2 |
| **Security** | Trivy | Apache 2.0 | `security/trivy/` | Phase 3 |
| **Security** | CrowdSec | MIT | `security/crowdsec/` | Phase 3 |
| **Security** | Falco | Apache 2.0 | `security/falco/` | Phase 3 |
| **Security** | Kyverno | Apache 2.0 | `security/kyverno/` | Phase 3 |
| **Networking** | VPC + DNS | — | `networking/` | Phase 1 |
| **Secrets** | Infisical | MIT | K8s Operator | Phase 1 |
| **Proxy** | Caddy / nginx | Apache 2.0 | Templates / Helm | Phase 1 |
| **TOTAL** | **28 tools** | **27/28 FOSS** | **14 modules** | |

### FOSS Compliance

| Priority | Score | Detail |
|----------|-------|--------|
| #1 Speed to Market | ✅ | One-command deploy |
| **#2 FOSS** | **10/10** | All tools OSI-approved |
| #3 Data Sovereignty | ✅ | State encryption, customer-isolated VPCs |
| #4 Cooperative | ✅ | Linux Foundation (OpenTofu), community-governed |

---

## Product Tiers (TBD: currently added for the sake of approx integration):

| Feature | 🟢 Lite AI | 🔵 Pro AI |
|---------|-----------|----------|
| **Price** | $197/year | $1,997/year |
| **Infrastructure** | DO Droplet | DOKS Cluster (K8s) |
| **GPU** | Shared GPU/CPU  | High quality GPU instance  (hosted on MI300X) |
| **Persistence** | Droplet-local | Persistent volumes + backups |
| **Database** | SQLite (embedded) | Managed PostgreSQL |
| **Redundancy** | None | Custom failover |
| **SLA** | Best effort | Highest tier |
| **Models** | Open-source (8B-14B) | State-of-the-art (70B+) |
| **Observability** | Shared Uptime Kuma | Dedicated Langfuse + Kuma |
| **Compliance** | — | ISO 42001 + ISO 27001 |
| **Support** | Email / Chat | AI Voice + DevOps |
| **Deploy command** | `weown-cli deploy` | `` |

---

## Directory Structure

```
iac/
├── README.md
│
├── opentofu/
│   ├── modules/
│   │   ├── droplet/                    # Single Droplet (Lite pipeline)
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── templates/
│   │   ├── doks/                       # DOKS Cluster (Pro pipeline)
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── networking/                 # VPC + DNS + DO Project
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       ├── outputs.tf
│   │       ├── database/               # Managed PostgreSQL v18
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── gpu/                    # MI300X / MI325X provisioning
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       └── internal-tools/         # 🆕 Internal services
│   │           └── n8n/
│   │               ├── main.tf
│   │               ├── variables.tf
│   │               └── outputs.tf
│
│   └── environments/                   # Environment definitions (e.g., dev, staging, prod)
│   │   └── vaultwarden/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   │
├── collaboration/              # 🆕 Planned services
|   ├── matomo/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── nextcloud/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── mail/
│   │   ├── stalwart/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── postal/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   │
│   │   ├── observability/              # 🔄 EXPANDED
│   │   │   ├── uptime-kuma/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── langfuse/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── grafana-alloy/          # 🆕 Replaces Promtail
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── mimir/                  # 🆕 Long-term metrics
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   │
│   │   ├── gitops/                     # 🆕 GitOps + auto-update
│   │   │   ├── argocd/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── watchtower/
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   │
│   │   └── security/                   # 🆕 Security stack
│   │       ├── trivy/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── crowdsec/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       ├── falco/
│   │       │   ├── main.tf
│   │       │   ├── variables.tf
│   │       │   └── outputs.tf
│   │       └── kyverno/
│   │           ├── main.tf
│   │           ├── variables.tf
│   │           └── outputs.tf
│
├── environments/
│   ├── lite/                       # WeOwn Lite
│   └── pro/                        # WeOwn Pro (includes all @RMN additions)
│
└── scripts/
    └── deploy-pro.sh
```

---

## Prerequisites

### Required Tools

| Tool | Version | Install |
|------|---------|---------|
| OpenTofu | ≥ 1.6.0 | [opentofu.org/docs/intro/install](https://opentofu.org/docs/intro/install/) |
| doctl | Latest | [docs.digitalocean.com/reference/doctl](https://docs.digitalocean.com/reference/doctl/how-to/install/) |
| kubectl | ≥ 1.28 | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) |
| Helm | ≥ 3.12 | [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/) |
| jq | Latest | `apt install jq` / `brew install jq` |

### Required Accounts & Credentials

| Credential | Source | Env Variable |
|------------|--------|-------------|
| DO API Token | [cloud.digitalocean.com/account/api/tokens](https://cloud.digitalocean.com/account/api/tokens) | `DIGITALOCEAN_TOKEN` |
| DO Spaces Key | DO Spaces access key | `AWS_ACCESS_KEY_ID` |
| DO Spaces Secret | DO Spaces secret key | `AWS_SECRET_ACCESS_KEY` |
| Infisical Client ID | Infisical dashboard | `TF_VAR_infisical_client_id` |
| Infisical Client Secret | Infisical dashboard | `TF_VAR_infisical_client_secret` |
| SSH Key ID | `doctl compute ssh-key list` | Passed as variable |

### Verify Installation

```bash
# Verify all tools
tofu version        # OpenTofu v1.6.0+
doctl version       # doctl 1.x
kubectl version     # Client v1.28+
helm version        # v3.12+

# Verify DO authentication
doctl auth init
doctl account get

# Verify Spaces access
doctl s3 ls --endpoint-url https://atl1.digitaloceanspaces.com s3://weown-tofu-state/
```

---

## Quick Start

### Deploy WeOwn Lite AI (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/CCCbotNet/jaimsnet.git
cd jaimsnet/iac/weown-cli

# 2. Install the CLI Management Tool
uv pip install -e .
# OR: pip install -e .

# 3. Deploy interactively (Will prompt for DO Token if not set via doctl)
weown-cli deploy

# 4. Check status and tail logs
weown-cli list
weown-cli logs <deployment-name>
```

### Deploy WeOwn Pro AI (15 minutes)

```bash
# 1. Set credentials (same as above)

# 2. Deploy
./scripts/deploy-pro.sh acme acme.pro.weown.agency

# 3. Get kubeconfig
export KUBECONFIG=./environments/pro/kubeconfig-doks-acme.yaml

# 4. Verify cluster
kubectl get nodes
kubectl get pods -A

# 5. Verify endpoint
curl -I https://acme.pro.weown.agency
# Expected: HTTP/2 200
```

### Destroy (Decommission)

```bash
# Lite
cd jaimsnet/iac/weown-cli
weown-cli destroy <deployment-name>

# Pro
cd environments/pro
tofu destroy -var="customer_slug=acme" \
             -var="customer_domain=acme.pro.weown.agency" \
             -var="customer_name=acme"
```

---

## Module Reference

### `modules/droplet`

Provisions a single DO Droplet with AnythingLLM + Caddy via cloud-init.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `instance_name` | string | — | Droplet name |
| `domain` | string | — | Full domain (e.g., `acme.weown.tools`) |
| `dns_zone` | string | — | DNS zone (e.g., `weown.tools`) |
| `dns_subdomain` | string | — | Subdomain (e.g., `acme`) |
| `region` | string | `atl1` | DO region |
| `droplet_size` | string | `s-2vcpu-4gb` | Droplet size slug |
| `ssh_key_ids` | list(string) | — | SSH key IDs |
| `tier` | string | `lite` | Product tier (`lite` or `pro`) |
| `enable_backups` | bool | `false` | Enable DO backups |

| Output | Description |
|--------|-------------|
| `droplet_id` | Droplet resource ID |
| `ipv4_address` | Public IPv4 |
| `instance_url` | Full HTTPS URL |
| `firewall_id` | Firewall resource ID |
| `dns_record_fqdn` | DNS FQDN |

### `modules/doks`

Provisions a managed Kubernetes cluster with autoscaling.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `cluster_name` | string | — | DOKS cluster name |
| `region` | string | `atl1` | DO region |
| `k8s_version` | string | `1.31.1-do.5` | K8s version |
| `node_size` | string | `s-4vcpu-8gb` | Node pool size |
| `autoscale_min` | number | `1` | Min nodes |
| `autoscale_max` | number | `3` | Max nodes |

| Output | Description |
|--------|-------------|
| `cluster_id` | DOKS cluster ID |
| `cluster_endpoint` | K8s API endpoint (sensitive) |
| `kubeconfig_raw` | Raw kubeconfig (sensitive) |
| `cluster_urn` | DO resource URN |

### `modules/networking`

Provisions VPC, DNS zone, and DO Project.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `vpc_name` | string | `weown-vpc` | VPC name |
| `region` | string | `atl1` | DO region |
| `vpc_ip_range` | string | `10.10.10.0/24` | VPC CIDR |

| Output | Description |
|--------|-------------|
| `vpc_id` | VPC UUID |
| `vpc_urn` | VPC URN |

### `modules/database`

Provisions managed PostgreSQL with multiple databases and firewall rules.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `cluster_name` | string | `db-weown` | DB cluster name |
| `pg_version` | string | `18` | PostgreSQL version |
| `db_size` | string | `db-s-1vcpu-1gb` | Plan size |
| `database_names` | list(string) | `["litellm","langfuse"]` | Databases to create |
| `trusted_sources` | list(object) | `[]` | Firewall trusted sources |

| Output | Description |
|--------|-------------|
| `cluster_id` | DB cluster ID |
| `host` | Connection host (sensitive) |
| `port` | Connection port |
| `connection_uri` | Full URI (sensitive) |

---

## Environment Configuration

### Lite — Override per Customer

```bash
tofu apply \
  -var="customer_slug=acme" \
  -var="customer_name=Acme Corp" \
  -var="customer_domain=acme.weown.tools" \
  -var="dns_subdomain=acme" \
  -var="ssh_key_ids=[\"12345678\"]"
```

### Pro — Override per Customer

```bash
tofu apply \
  -var="customer_slug=acme" \
  -var="customer_name=Acme Corp" \
  -var="customer_domain=acme.pro.weown.agency" \
  -var="autoscale_max=5" \
  -var="db_size=db-s-2vcpu-4gb"
```

---

## State Management

| Field | Value |
|-------|-------|
| Backend | DO Spaces (S3-compatible) |
| Bucket | `weown-tofu-state` |
| Region | ATL1 |
| Encryption | ✅ AES-GCM at rest (OpenTofu-exclusive) |
| Locking | ✅ Enabled |
| Versioning | ✅ DO Spaces versioning |
| Key format | `<tier>/<customer_slug>/terraform.tfstate` |

### State Isolation

```
weown-tofu-state/
├── lite/
│   ├── acme/terraform.tfstate
│   ├── client2/terraform.tfstate
│   └── client3/terraform.tfstate
└── pro/
    ├── enterprise1/terraform.tfstate
    └── enterprise2/terraform.tfstate
```

> **Each customer gets isolated state.** No cross-contamination.

---

## Secrets Management

| Secret | Source | Method |
|--------|--------|--------|
| DO API Token | Infisical | Provider data source |
| DO Spaces credentials | Environment variables | `DIGITALOCEAN_TOKEN` 
| SSH keys | DO account | Referenced by ID |
| State encryption passphrase | Infisical | `TF_VAR_state_encryption_passphrase` |

> **No secrets in Git. Ever.** All credentials via Infisical or environment variables.

---

## Deployment Guide

> This section covers the full, step-by-step procedures to deploy and tear down all jAIMSnet infrastructure components using `weown-cli` and OpenTofu. Follow the dependency order carefully — infrastructure must be provisioned before application stacks.

---

### Phase 0 — Prerequisites & Authentication

#### 1. Install required tools

```bash
# OpenTofu (IaC)
brew install opentofu          # macOS
# or: https://opentofu.org/docs/intro/install/

# DigitalOcean CLI
brew install doctl             # macOS
# or: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Kubernetes CLI
brew install kubectl

# Helm (K8s package manager)
brew install helm

# weown-cli (this repo's management tool)
cd iac/weown-cli
uv pip install -e .
# or: pip install -e .
```

#### 2. Authenticate DigitalOcean

```bash
# One-time auth (saves token to ~/.config/doctl/config.yaml)
doctl auth init

# Verify authentication
doctl account get
# Expected: your DO account email + status

# Verify the context name (used by weown-cli internally)
doctl auth list
# Note the context name in use (e.g. ldc-account-weown)
```

#### 3. Set up Infisical Machine Identity (Secrets Management)

Create a Machine Identity in [Infisical Cloud → Settings → Machine Identities](https://app.infisical.com):
1. Create a new Machine Identity with **Universal Auth**
2. Assign it to the `jaimsnet` project with **Reader** access
3. Generate a **Client Secret**

Store the credentials securely (they will be injected into the cluster as a K8s secret):

```bash
# These are NOT committed to Git.
# Store them in your local .env or Infisical itself for bootstrapping.
export INFISICAL_CLIENT_ID="<your-machine-identity-client-id>"
export INFISICAL_CLIENT_SECRET="<your-machine-identity-client-secret>"
```

> ⚠️ The `projectSlug` used in `InfisicalSecret` manifests is `jaimsnet` (configured in `iac/k8s/infisical-config.yaml`). Make sure your Machine Identity has access to paths `/gateway/*` and `/observability/*`.

---

### Phase 1 — Core Infrastructure (DOKS, VPC, PostgreSQL, Load Balancer)

This provisions the DigitalOcean Kubernetes cluster and shared infrastructure components via OpenTofu.

#### 1. Initialize OpenTofu backend

```bash
cd iac/opentofu/environments/production

# Initialize backend (connects to DO Spaces state bucket)
export DIGITALOCEAN_TOKEN="$(doctl auth init --access-token '' 2>&1 || doctl account get --format Token --no-header 2>/dev/null)"
# or set directly:
export DIGITALOCEAN_TOKEN="dop_v1_..."

tofu init
# Expected: "Terraform has been successfully initialized!"
```

#### 2. Plan (dry-run — review before applying)

```bash
tofu plan
# Review the plan output carefully:
# + digitalocean_kubernetes_cluster.jaimsnet_core_doks
# + digitalocean_database_cluster.jaimsnet_pg
# + digitalocean_vpc.jaimsnet_vpc
# + digitalocean_loadbalancer.jaimsnet_lb
```

#### 3. Apply (provision infrastructure)

```bash
tofu apply -auto-approve
# Duration: ~10-15 minutes
# Expected final output:
# Apply complete! Resources: N added, 0 changed, 0 destroyed.
```

#### 4. Verify DOKS cluster is reachable

```bash
# weown-cli fetches and saves kubeconfig automatically
weown-cli gateway status --cluster jaimsnet-core-doks

# Or manually via doctl
doctl kubernetes cluster kubeconfig save jaimsnet-core-doks
kubectl get nodes
# Expected: node(s) in Ready state
```

---

### Phase 2 — Cluster Baseline (Ingress + TLS + Infisical Operator)

Install shared cluster services that all application workloads depend on.

#### 1. Install Ingress NGINX Controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --wait
# Wait: ~2-3 minutes until LoadBalancer IP is assigned

# Verify
kubectl get svc -n ingress-nginx ingress-nginx-controller
# Note the EXTERNAL-IP — this is your cluster's public IP
```

#### 2. Install cert-manager (TLS automation)

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true \
  --wait

# Verify
kubectl get pods -n cert-manager
```

#### 3. Apply ClusterIssuer (Let's Encrypt)

```bash
# Edit ingress/clusterissuer.yaml — set your email address
kubectl apply -f ingress/clusterissuer.yaml

# Verify
kubectl get clusterissuer letsencrypt-prod
# Expected: READY = True
```

#### 4. Install Infisical Secrets Operator

```bash
helm repo add infisical-helm-charts 'https://dl.cloudsmith.io/public/infisical/helm-charts/helm/charts/'
helm repo update

helm install infisical-operator infisical-helm-charts/secrets-operator \
  --namespace infisical \
  --create-namespace \
  --wait

# Verify CRDs are installed
kubectl get crd | grep infisical
# Expected: infisicalsecrets.secrets.infisical.com  listed

# Verify operator pod is running
kubectl get pods -n infisical
```

#### 5. Inject Infisical Machine Identity credentials into the cluster

```bash
# This K8s secret is referenced by all InfisicalSecret manifests
kubectl create secret generic universal-auth-credentials \
  --namespace infisical \
  --from-literal=clientId="$INFISICAL_CLIENT_ID" \
  --from-literal=clientSecret="$INFISICAL_CLIENT_SECRET"

# Verify (should show clientId and clientSecret keys)
kubectl get secret universal-auth-credentials -n infisical -o jsonpath='{.data}' | \
  python3 -c "import sys,json,base64; d=json.load(sys.stdin); print({k: base64.b64decode(v).decode()[:8]+'...' for k,v in d.items()})"
```

#### 6. Apply shared Infisical ConfigMap

```bash
# Stores project slug and env — referenced in documentation
kubectl apply -f iac/k8s/infisical-config.yaml
```

---

### Phase 3 — Gateway Stack (Redis → Langfuse → LiteLLM → AnythingLLM)

Deploy the AI Gateway application stack using `weown-cli`. The CLI applies manifests in dependency order.

```bash
# Full stack rollout (all phases)
export DIGITALOCEAN_TOKEN="dop_v1_..."

weown-cli gateway deploy --cluster jaimsnet-core-doks --yes
```

The deployment proceeds in phases:
1. **Namespaces** — `gateway`, `anythingllm`, `observability`
2. **Infisical Secret Syncs** — syncs secrets from Infisical Cloud into each namespace's K8s `Secret`
3. **Redis Cache** — StatefulSet with PVC, waits for Infisical `redis-secrets` to exist
4. **Langfuse Observability** — Deployment + Ingress (`langfuse.jaims.app`)
5. **LiteLLM Gateway** — Deployment + Ingress + ConfigMap (`litellm.jaims.app`)
6. **AnythingLLM UI** — Deployment + PVC + Ingress (`anythingllm.jaims.app`)

> ⚠️ **Prerequisite**: Phases 1 and 2 must be complete. The Infisical Machine Identity must have access to:
> - `/gateway/redis`, `/gateway/litellm`, `/gateway/anythingllm`
> - `/observability/langfuse`

---

### Phase 4 — Verification

After deployment completes, verify all components:

```bash
# Check all gateway pods
kubectl get pods -n gateway
kubectl get pods -n observability
kubectl get pods -n anythingllm
# All pods should be in Running state (not CrashLoopBackOff / CreateContainerConfigError)

# Check Infisical secret sync status
kubectl get infisicalsecrets -A
# SYNCED column should be True for all

# Check ingress endpoints
kubectl get ingress -A
# Should show hosts: litellm.jaims.app, langfuse.jaims.app, anythingllm.jaims.app

# Check TLS certificate issuance
kubectl get certificate -A
# READY = True means Let's Encrypt cert issued

# Smoke test HTTP endpoints
curl -I https://langfuse.jaims.app      # 200 OK
curl -I https://litellm.jaims.app/health  # {"status": "ok"}

# Full status via weown-cli
weown-cli gateway status --cluster jaimsnet-core-doks
```

---

### Lite Droplet Deployment (WeOwn Lite AI tier)

For deploying a single customer AnythingLLM instance on a DO Droplet (not K8s):

```bash
# 1. Install CLI
cd iac/weown-cli && uv pip install -e .

# 2. Authenticate
doctl auth init  # one-time only

# 3. Deploy interactively
weown-cli deploy
# Prompts for: customer name, domain, region, SSH key

# 4. Monitor
weown-cli list                     # See all deployments
weown-cli logs <deployment-name>   # Tail cloud-init logs

# 5. Verify
curl -I https://<customer-domain>  # HTTP/2 200
```

---

### Step-by-Step: Pro (DOKS per-customer)

```bash
# 1. Navigate to environment
cd iac/opentofu/environments/pro

# 2. Initialize
tofu init

# 3. Plan with customer variables
tofu plan \
  -var="customer_slug=acme" \
  -var="customer_name=Acme Corp" \
  -var="customer_domain=acme.pro.weown.agency" \
  -var="autoscale_max=3"

# 4. Apply
tofu apply -auto-approve

# 5. Save kubeconfig
doctl kubernetes cluster kubeconfig save doks-acme

# 6. Verify
kubectl get nodes
kubectl get pods -A

# 7. Verify endpoint
curl -I https://acme.pro.weown.agency
# Expected: HTTP/2 200
```

---

### Teardown — Gateway Stack (Application Layer Only)

Removes all Kubernetes application resources without touching core infrastructure (DOKS, PostgreSQL, VPC remain).

```bash
# Remove all gateway application resources
# Order: AnythingLLM → LiteLLM → Langfuse → Redis → namespaces
weown-cli gateway destroy --cluster jaimsnet-core-doks --yes

# Verify all application pods removed
kubectl get pods -A | grep -E "gateway|observability|anythingllm"
# Should return empty

# Optionally clean up Infisical operator
helm uninstall infisical-operator -n infisical
```

### Teardown — Core Infrastructure (via OpenTofu)

> ⚠️ **Destructive** — removes DOKS cluster, managed PostgreSQL, VPC, and Load Balancer. All data in the database will be lost.

```bash
cd iac/opentofu/environments/production

# Review what will be destroyed
tofu plan -destroy

# Destroy all core infrastructure
tofu destroy -auto-approve
# Duration: ~10-15 minutes
# Expected: "Destroy complete! Resources: N destroyed."

# Verify in DigitalOcean console
doctl kubernetes cluster list    # should be empty
doctl database list              # should be empty
```

### Teardown — Lite Droplet

```bash
# Destroy a specific droplet deployment
weown-cli destroy <deployment-name>

# Verify
doctl compute droplet list | grep <deployment-name>
# Should return empty
```

---

## Testing

### Pre-Deploy Validation

```bash
# Validate HCL syntax
tofu validate

# Format check
tofu fmt -check -recursive

# Plan (dry run)
tofu plan -var="customer_slug=test" \
          -var="customer_domain=test.weown.tools" \
          -var="customer_name=Test" \
          -var="dns_subdomain=test"
```

### Smoke Test (10-Point)

| # | Test | Command | Expected |
|---|------|---------|----------|
| 1 | `tofu init` succeeds | `tofu init` | Backend connected |
| 2 | `tofu validate` passes | `tofu validate` | "Success!" |
| 3 | `tofu plan` — no errors | `tofu plan` | Valid plan output |
| 4 | State encrypted | Check DO Spaces | Encrypted blob |
| 5 | Infisical secrets resolve | `tofu plan` (no auth errors) | Providers authenticated |
| 6 | Create test Droplet | `tofu apply` (test env) | Droplet appears in DO |
| 7 | DNS resolves | `dig test.weown.tools` | Returns IP |
| 8 | HTTPS works | `curl -I https://test.weown.tools` | HTTP/2 200 |
| 9 | AnythingLLM responds | Browser → admin panel | Login page |
| 10 | Destroy clean | `tofu destroy` | All resources removed |

### Integration Test — Full Cycle

```bash
# Install
cd weown-cli
pip install -e .

# Deploy
weown-cli deploy  # Follow the interactive prompts

# Verify
curl -sf https://<deployment-name>.weown.tools && echo "✅ PASS" || echo "❌ FAIL"

# Destroy
weown-cli destroy <deployment-name>

echo "✅ Full cycle complete"
```

---

## CI/CD — GitHub Actions

### Workflow: Plan on PR, Apply on Merge

```yaml
# Triggered by changes to iac/ directory
# PR → tofu plan (review in PR comments)
# Merge to main → tofu apply (auto-deploy)
```

| Event | Action | Approval |
|-------|--------|----------|
| Pull Request | `tofu plan` — output in PR | Team reviews |
| Merge to main | `tofu apply` — infrastructure deployed | Auto (post-review) |

### Required Secrets

| Secret | Description |
|--------|-------------|
| `DIGITALOCEAN_TOKEN` | DO API token |
| `DO_SPACES_KEY` | Spaces access key |
| `DO_SPACES_SECRET` | Spaces secret key |
| `INFISICAL_CLIENT_ID` | Infisical machine identity |
| `INFISICAL_CLIENT_SECRET` | Infisical machine secret |

---

## Networking & Security

### VPC Isolation

| Tier | VPC CIDR | Isolation |
|------|----------|-----------|
| Lite | `10.10.20.0/24` | Shared VPC |
| Pro | `10.10.30.0/24` | Per-customer VPC |

### Firewall Rules (Lite — Droplet)

| Direction | Protocol | Port | Source |
|-----------|----------|------|--------|
| Inbound | TCP | 22 | SSH allowed IPs |
| Inbound | TCP | 80 | `0.0.0.0/0` |
| Inbound | TCP | 443 | `0.0.0.0/0` |
| Outbound | TCP/UDP | All | `0.0.0.0/0` |

### Security Hardening (cloud-init)

| # | Measure | Implementation |
|---|---------|---------------|
| 1 | SSH key auth only | cloud-init (no password) |
| 2 | UFW firewall | Ports 22, 80, 443 only |
| 3 | Fail2ban | Brute-force protection |
| 4 | Auto-updates | `unattended-upgrades` |
| 5 | Docker rootless | Container isolation |

---

## Internal Tools
### n8n — Workflow Automation

| Field | Value |
|-------|-------|
| Purpose | RAG chunking, webhook pipelines, API orchestration |
| License | ⚠️ Sustainable Use (fair-code — NOT OSI) |
| Module | `modules/internal-tools/n8n/` |
| Deployment | Docker (Droplet) or Helm (DOKS) |
| Database | PostgreSQL (shared managed instance) |
| Domain | `n8n.weown.agency` |

### Vaultwarden — Password Management

| Field | Value |
|-------|-------|
| Purpose | Self-hosted Bitwarden-compatible password vault |
| License | AGPL-3.0 ✅ |
| Module | `modules/internal-tools/vaultwarden/` |
| Deployment | Docker (Droplet) |
| Storage | SQLite or PostgreSQL |
| Domain | `vault.weown.tools` |

---

## Collaboration Services (Planned)

### Matomo — Self-Hosted Analytics

| Field | Value |
|-------|-------|
| Purpose | Privacy-respecting web analytics (GA alternative) |
| License | GPL-3.0 ✅ |
| Module | `modules/collaboration/matomo/` |
| Phase | P2 (W14+) |

### Nextcloud — File Storage & Collaboration

| Field | Value |
|-------|-------|
| Purpose | Self-hosted file sync, sharing, collaboration |
| License | AGPL-3.0 ✅ |
| Module | `modules/collaboration/nextcloud/` |
| Phase | P2 (W14+) |

### Stalwart — Email Server

| Field | Value |
|-------|-------|
| Purpose | Self-hosted SMTP/IMAP/JMAP email server |
| License | AGPL-3.0 ✅ |
| Module | `modules/collaboration/mail/stalwart/` |
| Phase | P2 (evaluate vs Proton Business) |

### Postal — Mail Delivery Platform

| Field | Value |
|-------|-------|
| Purpose | Self-hosted transactional + bulk email delivery |
| License | MIT ✅ |
| Module | `modules/collaboration/mail/postal/` |
| Phase | P2 (evaluate vs Proton Business) |

---

## Observability Stack (Expanded)

### Grafana — Telemetry Collector

| Field | Value |
|-------|-------|
| Purpose | Unified telemetry collector |
| License | Apache 2.0 ✅ |
| Module | `modules/observability/grafana-alloy/` |
| Collects | Logs + metrics + traces (OTLP, Prometheus, Loki) |

### Mimir — Long-Term Metrics Storage

| Field | Value |
|-------|-------|
| Purpose | Scalable long-term Prometheus metrics storage |
| License | AGPL-3.0 ✅ |
| Module | `modules/observability/mimir/` |
| Integrates | Prometheus → Mimir (remote write) → Grafana (query) |

### Full Observability Stack (jAIMSnet)

```
Layer 1 (Infrastructure):
  Prometheus → Mimir (long-term) → Grafana (dashboards)
  Grafana Alloy (collector) → Loki (logs) → Grafana
  
Layer 2 (Endpoints):
  Uptime Kuma → Status pages + alerts

Layer 3 (AI/LLM):
  Langfuse → Prompt tracing + cost tracking
```

---

## GitOps & Deployment

### ArgoCD — GitOps Continuous Delivery

| Field | Value |
|-------|-------|
| Purpose | Declarative GitOps for Kubernetes |
| License | Apache 2.0 ✅ |
| Module | `modules/gitops/argocd/` |
| Workflow | Git push → ArgoCD detects → syncs to cluster |
| Phase | Phase 3 (jAIMSnet) |

### Watchtower — Container Auto-Update

| Field | Value |
|-------|-------|
| Purpose | Automatically update running Docker containers |
| License | Apache 2.0 ✅ |
| Module | `modules/gitops/watchtower/` |
| Scope | Droplet-based services (Lite tier + standalone) |
| Note | DOKS uses ArgoCD instead |

### GitOps Strategy

| Infrastructure | Tool | Trigger |
|---------------|------|---------|
| DOKS (K8s) | **ArgoCD** | Git push → auto-sync |
| Droplets (Docker) | **Watchtower** | Registry push → auto-pull |
| IaC (OpenTofu) | **GitHub Actions** | PR merge → tofu apply |

---

## Security Stack

### Trivy — Vulnerability Scanning

| Field | Value |
|-------|-------|
| Purpose | Container image + filesystem + IaC vulnerability scanning |
| License | Apache 2.0 ✅ |
| Module | `modules/security/trivy/` |
| Scope | CI/CD pipeline (pre-deploy scanning) + runtime |

### CrowdSec — Collaborative Threat Detection

| Field | Value |
|-------|-------|
| Purpose | Community-driven intrusion detection + prevention |
| License | MIT ✅ |
| Module | `modules/security/crowdsec/` |
| Scope | All public-facing endpoints |

### Falco — Runtime Security

| Field | Value |
|-------|-------|
| Purpose | K8s runtime threat detection (syscall monitoring) |
| License | Apache 2.0 ✅ |
| Module | `modules/security/falco/` |
| Scope | DOKS clusters (Pro tier) |

### Kyverno — K8s Policy Engine

| Field | Value |
|-------|-------|
| Purpose | Kubernetes admission controller + policy enforcement |
| License | Apache 2.0 ✅ |
| Module | `modules/security/kyverno/` |
| Scope | DOKS clusters (Pro tier) — enforce container policies |

### Security Layers

```
Build Phase:
  Trivy (scan images) → Block vulnerable deploys

Runtime Phase:
  CrowdSec (network threats) → Block malicious IPs
  Falco (syscall monitoring) → Alert on anomalies
  Kyverno (admission control) → Enforce policies
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `tofu init` fails — backend | Spaces credentials missing | Set `DIGITALOCEAN_TOKEN` |
| `tofu plan` — provider auth | DO token missing/expired | Set `DIGITALOCEAN_TOKEN` or rotate in Infisical |
| DNS not resolving | Propagation delay | Wait 5-10 min; verify with `dig` |
| SSL cert pending | Caddy needs DNS + port 80 | Ensure firewall allows 80/443; DNS resolves |
| Cloud-init not completing | Script error in user_data | SSH in → `cat /var/log/cloud-init-output.log` |
| State lock error | Concurrent apply | Wait or force-unlock: `tofu force-unlock <ID>` |
| DOKS nodes not scaling | Autoscaler limits | Check `autoscale_min`/`autoscale_max` in tfvars |

---

## Contributing

1. **Branch** from `main` — never commit directly
2. **Write HCL** in the appropriate module or environment
3. **Validate** — `tofu fmt && tofu validate`
4. **Open PR** — GitHub Actions runs `tofu plan`
5. **Review** — team reviews plan output in PR
6. **Merge** — auto-applies via GitHub Actions
7. **No secrets in Git** — use Infisical or env vars

### Naming Conventions

| Resource | Pattern | Example |
|----------|---------|---------|
| Droplet | `<tool>-<ccc-id-name>` | `anythingllm-ldc` |
| DOKS | `doks-<ccc-id-name>` | `doks-ldc` |
| Database | `db-<ccc-id-name>` | `db-ldc` |
| VPC | `weown-<ccc-id-name>-vpc` | `weown-ldc-vpc` |
| Firewall | `<instance>-fw` | `anythingllm-ldc-fw` |
| State key | `<ccc-id-name>/terraform.tfstate` | `ldc/terraform.tfstate` |

---

## Related Projects

| Project | Description | URL |
|---------|-------------|-----|
| PRJ-015 | #HybridArchitecture — GPU instances | [GitHub](https://github.com/CCCbotNet/fedarch/blob/main/_PROJECTS_/PRJ-015_HybridArchitecture.md) |
| PRJ-016 | LiteLLM AI Gateway | [GitHub](https://github.com/CCCbotNet/fedarch/blob/main/_PROJECTS_/PRJ-016_AIGateway-LiteLLM.md) |
| PRJ-017 | Langfuse Observability | [GitHub](https://github.com/CCCbotNet/fedarch/blob/main/_PROJECTS_/PRJ-017_Observability.md) |
| PRJ-032 | OpenTofu IaC for #FedArch | [GitHub](https://github.com/CCCbotNet/fedarch/blob/main/_PROJECTS_/PRJ-032_OpenTofu-IaC.md) |

---

## License

OpenTofu is licensed under the [MPL-2.0](https://github.com/opentofu/opentofu/blob/main/LICENSE) license.

