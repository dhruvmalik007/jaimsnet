terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

module "lite_droplet" {
  source = "../../modules/droplet"

  ssh_key_name      = var.ssh_key_name
  droplet_name      = var.customer_id
  region            = var.region
  droplet_size      = var.droplet_size
  enable_watchtower = var.enable_watchtower
  allowed_ssh_cidrs = var.allowed_ssh_cidrs
  allowed_api_cidrs = var.allowed_api_cidrs
  domain_name       = var.domain_name
}
