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
# 6. DigitalOcean Load Balancer
# ------------------------------------------------------------------------------
module "load_balancer" {
  source = "../../modules/load-balancer"

  name              = "jaimsnet-ingress-lb-${var.environment}"
  region            = var.region
  vpc_uuid          = module.vpc.vpc_id
  doks_cluster_name = module.doks.cluster_name

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

  doks_cluster_mappings = [
    for r in [
      { cluster_id = module.doks.cluster_name, record_name = "litellm", record_type = "A", lb_ip = module.load_balancer.lb_ip },
      { cluster_id = module.doks.cluster_name, record_name = "langfuse", record_type = "A", lb_ip = module.load_balancer.lb_ip },
      var.environment == "pro" ? { cluster_id = module.doks.cluster_name, record_name = "*", record_type = "A", lb_ip = module.load_balancer.lb_ip } : null
    ] : r if r != null
  ]

  droplet_mappings = [
    for r in [
      var.kuma_ip != "" ? { droplet_id = "kuma", record_name = "kuma", record_type = "A", value = var.kuma_ip } : null
    ] : r if r != null
  ]

  # Standard FedArch TXT records for SPF/DMARC policies
  # txt_records = {
  #   spf    = "v=spf1 include:_spf.google.com ~all"
  #   _dmarc = "v=DMARC1; p=quarantine; rua=mailto:security@${var.domain}"
  # }

  depends_on = [
    module.load_balancer
  ]
}


# ------------------------------------------------------------------------------
# 8. Uptime Kuma Monitoring Droplet
# ------------------------------------------------------------------------------
data "digitalocean_ssh_key" "prod_key" {
  name = var.ssh_key_name
}

module "uptime_kuma" {
  source = "../../modules/droplet"

  name        = "weown-ai-uptime-kuma"
  region      = var.region
  size        = "s-1vcpu-1gb" # Minimal droplet for Uptime Kuma
  vpc_uuid    = module.vpc.vpc_id
  tags        = ["weown-ai", "production", "monitoring", "uptime-kuma"]
  ssh_key_ids = [data.digitalocean_ssh_key.prod_key.id]

  user_data = templatefile("${path.module}/templates/cloudinit-uptime-kuma.yaml", {
    hostname = "uptime-kuma.jaims.app"
  })
}

resource "digitalocean_firewall" "weown_ai_monitoring" {
  name = "weown-ai-uptime-kuma-fw"

  droplet_ids = [module.uptime_kuma.droplet_id]

  # Allow SSH from authorized IP ranges
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.allowed_ssh_cidrs
  }

  # Uptime Kuma Web Dashboard
  inbound_rule {
    protocol         = "tcp"
    port_range       = "3001"
    source_addresses = ["0.0.0.0/0", "::/0"] # Can be restricted to specific IPs if needed
  }

  # Allow HTTP outbound (package updates, HTTP endpoints)
  outbound_rule {
    protocol              = "tcp"
    port_range            = "80"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow HTTPS outbound (package updates, HTTPS endpoints, webhooks)
  outbound_rule {
    protocol              = "tcp"
    port_range            = "443"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow DNS resolution
  outbound_rule {
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow outbound ICMP (pings to the outside world)
  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow unrestricted outbound to the internal VPC to monitor all services natively
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = [module.vpc.ip_range]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = [module.vpc.ip_range]
  }
}
