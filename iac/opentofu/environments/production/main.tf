# ------------------------------------------------------------------------------
# 1. VPC Network Setup
# ------------------------------------------------------------------------------
module "vpc" {
  source   = "../../modules/vpc"
  name     = "jaimsnet-${var.environment}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"
}

# ------------------------------------------------------------------------------
# 2. Database Cluster (using our local module)
# ------------------------------------------------------------------------------
module "database" {
  source = "../../modules/database"

  cluster_name = "jaimsnet-postgres-${var.environment}"
  region       = var.region
  size         = var.db_cluster_size
  node_count   = 1 # Primary only for Phase 1
  vpc_uuid     = module.vpc.vpc_id
}

# ------------------------------------------------------------------------------
# 3. DigitalOcean Kubernetes (DOKS) Cluster
# ------------------------------------------------------------------------------
# We query the latest DO K8s version if 'latest' is passed
data "digitalocean_kubernetes_versions" "core" {
  version_prefix = var.doks_cluster_version == "latest" ? "" : var.doks_cluster_version
}

module "doks" {
  source = "../../modules/doks-cluster"

  cluster_name   = "jaimsnet-${var.environment}-doks"
  region         = var.region
  k8s_version    = data.digitalocean_kubernetes_versions.core.latest_version
  vpc_uuid       = module.vpc.vpc_id
  node_size      = var.doks_node_size
  node_min_count = var.doks_min_nodes
  node_max_count = var.doks_max_nodes

  tags = [
    "project:weown-ai",
    "compliance:fedarch",
    "env:${var.environment}"
  ]
}

# ------------------------------------------------------------------------------
# 4. ArgoCD Bootstrap via Helm
# ------------------------------------------------------------------------------
# Create the argocd namespace first
resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
  depends_on = [module.doks]
}

# Install ArgoCD via official Helm chart
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "6.6.0" # Use a stable chart version 
  namespace  = kubernetes_namespace.argocd.metadata[0].name

  values = [
    yamlencode({
      server = {
        service = {
          type = "ClusterIP"
        }
        insecure = true
      }
    })
  ]

  depends_on = [
    kubernetes_namespace.argocd
  ]
}

# ------------------------------------------------------------------------------
# 5. GitOps Bootstrap (App of Apps Pattern)
# ------------------------------------------------------------------------------
resource "helm_release" "argocd_apps" {
  name       = "argocd-apps"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argocd-apps"
  version    = "1.4.1"
  namespace  = kubernetes_namespace.argocd.metadata[0].name

  depends_on = [
    helm_release.argocd
  ]

  values = [
    yamlencode({
      applications = {
        jaimsnet-root = {
          namespace = "argocd"
          project   = "default"
          source = {
            repoURL        = "https://github.com/dhruvmalik007/jaimsnet.git"
            targetRevision = "HEAD"
            path           = "k8s/bootstrap"
          }
          destination = {
            server    = "https://kubernetes.default.svc"
            namespace = "argocd" # Deploys further applications into Argo namespace
          }
          syncPolicy = {
            automated = {
              prune    = true
              selfHeal = true
            }
          }
        }
      }
    })
  ]
}

# ------------------------------------------------------------------------------
# 6. DigitalOcean Load Balancer
# ------------------------------------------------------------------------------
module "load_balancer" {
  source = "../../modules/load-balancer"

  name            = "jaimsnet-ingress-lb-${var.environment}"
  region          = var.region
  vpc_uuid        = module.vpc.vpc_id
  doks_cluster_id = module.doks.cluster_id

  # Default ingress-nginx port routing configuration
  http_node_port  = 30080
  https_node_port = 30443
}

# ------------------------------------------------------------------------------
# 7. Custom DNS Provisioning
# ------------------------------------------------------------------------------
module "dns" {
  source = "../../modules/dns"
  count  = var.domain != "" ? 1 : 0

  domain = var.domain
  lb_ip  = module.load_balancer.lb_ip

  # Conditionally build the list of DNS records based on the fedarch and weown lite/pro setup
  records = [
    for r in [
      { name = "litellm", type = "A", value = "use_lb_ip" },
      { name = "langfuse", type = "A", value = "use_lb_ip" },
      var.environment == "pro" ? { name = "*", type = "A", value = "use_lb_ip" } : null,
      var.kuma_ip != "" ? { name = "kuma", type = "A", value = var.kuma_ip } : null
    ] : r if r != null
  ]

  # Standard FedArch TXT records for SPF/DMARC policies
  txt_records = {
    spf    = "v=spf1 include:_spf.google.com ~all"
    _dmarc = "v=DMARC1; p=quarantine; rua=mailto:security@${var.domain}"
  }

  depends_on = [
    module.load_balancer
  ]
}
