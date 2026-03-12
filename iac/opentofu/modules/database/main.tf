terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

resource "digitalocean_database_cluster" "postgres" {
  name                 = var.cluster_name
  engine               = "pg"
  version              = "16"
  size                 = var.size
  region               = var.region
  node_count           = var.node_count
  private_network_uuid = var.vpc_uuid
}

resource "digitalocean_database_db" "litellm" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "litellm"
}

resource "digitalocean_database_db" "langfuse" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "langfuse"
}

resource "digitalocean_database_user" "litellm" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "litellm_user"
}

resource "digitalocean_database_user" "langfuse" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "langfuse_user"
}

resource "digitalocean_database_firewall" "postgres_fw" {
  cluster_id = digitalocean_database_cluster.postgres.id

  rule {
    type  = "vpc"
    value = var.vpc_uuid
  }
}
