terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

resource "digitalocean_kubernetes_cluster" "cluster" {
  name    = var.cluster_name
  region  = var.region
  version = var.k8s_version

  vpc_uuid = var.vpc_uuid
  tags     = var.tags

  # Automatically upgrade the cluster and nodes to the latest patch release
  auto_upgrade = true

  # Ensure the cluster runs highly available control plane processes
  ha = false # DO limits HA to specific sizes, keep false for lite, but configurable if needed

  node_pool {
    name       = "${var.cluster_name}-default-pool"
    size       = var.node_size
    auto_scale = true
    min_nodes  = var.node_min_count
    max_nodes  = var.node_max_count
    tags       = var.tags
  }
}
