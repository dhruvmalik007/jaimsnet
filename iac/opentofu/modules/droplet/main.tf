terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

resource "digitalocean_droplet" "this" {
  name       = var.name
  image      = var.image
  region     = var.region
  size       = var.size
  vpc_uuid   = var.vpc_uuid != "" ? var.vpc_uuid : null
  ssh_keys   = var.ssh_key_ids
  tags       = var.tags
  user_data  = var.user_data
  monitoring = true
  ipv6       = true

  lifecycle {
    create_before_destroy = true
  }
}
