terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

resource "digitalocean_vpc" "vpc" {
  name        = var.name
  region      = var.region
  ip_range    = var.ip_range
  description = "Secure isolated VPC network"
}
