terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

# Fetch the DOKS cluster tags
data "digitalocean_kubernetes_cluster" "doks" {
  name = var.doks_cluster_id
}

# Fetch all Droplets matching the DOKS cluster tag
data "digitalocean_droplets" "doks_nodes" {
  filter {
    key    = "tags"
    values = [data.digitalocean_kubernetes_cluster.doks.urn]
  }
  filter {
    key    = "status"
    values = ["active"]
  }
}

# Local variable for droplet IDs array
locals {
  doks_node_ids = data.digitalocean_droplets.doks_nodes.droplets[*].id
}

resource "digitalocean_loadbalancer" "lb" {
  name        = var.name
  region      = var.region
  vpc_uuid    = var.vpc_uuid
  
  # Forward HTTP 80 -> Ingress HTTP NodePort
  forwarding_rule {
    entry_protocol  = "http"
    entry_port      = 80
    target_protocol = "http"
    target_port     = var.http_node_port
  }

  # Forward HTTPS 443 -> Ingress HTTPS NodePort (pass-through)
  forwarding_rule {
    entry_protocol  = "https"
    entry_port      = 443
    target_protocol = "https"
    target_port     = var.https_node_port
  }

  healthcheck {
    port                     = var.http_node_port
    protocol                 = "http"
    path                     = "/healthz"
    check_interval_seconds   = 10
    response_timeout_seconds = 5
    unhealthy_threshold      = 3
    healthy_threshold        = 2
  }

  droplet_ids = local.doks_node_ids
}
