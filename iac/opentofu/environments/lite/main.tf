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
}

data "digitalocean_ssh_key" "deployer" {
  name = var.ssh_key_name
}

module "lite_droplet" {
  source = "../../modules/droplet"

  name        = "${var.customer_id}-anythingllm"
  region      = var.region
  size        = var.droplet_size
  ssh_key_ids = [data.digitalocean_ssh_key.deployer.id]
  tags        = ["anythingllm", "weown-ai-lite", "docker"]

  user_data = templatefile("${path.module}/templates/cloudinit.yaml", {
    hostname          = "${var.customer_id}-anythingllm"
    enable_watchtower = var.enable_watchtower
    fqdn              = var.domain_name != "" ? "${var.customer_id}.${var.domain_name}" : ""
    litellm_base_url  = var.litellm_base_url
    litellm_api_key   = var.litellm_api_key
  })
}

resource "digitalocean_firewall" "anythingllm" {
  name = "${var.customer_id}-firewall"

  droplet_ids = [module.lite_droplet.droplet_id]

  # Allow SSH
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.allowed_ssh_cidrs
  }

  # Allow HTTP for Web / Caddy
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow HTTPS for Web / Caddy
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow AnythingLLM Direct Port
  inbound_rule {
    protocol         = "tcp"
    port_range       = "3001"
    source_addresses = var.allowed_api_cidrs
  }

  # Allow Ollama (Optional User Endpoints)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "11434"
    source_addresses = var.allowed_api_cidrs
  }

  # Allow LiteLLM Gateway (Optional User Endpoints)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "4000"
    source_addresses = var.allowed_api_cidrs
  }

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

  outbound_rule {
    protocol              = "tcp"
    port_range            = "80"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "443"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# --- DNS Integration ---

data "digitalocean_domain" "managed" {
  count = var.domain_name != "" ? 1 : 0
  name  = var.domain_name
}

resource "digitalocean_record" "anythingllm_a_record" {
  count  = var.domain_name != "" ? 1 : 0
  domain = data.digitalocean_domain.managed[0].name
  type   = "A"
  name   = var.customer_id
  value  = module.lite_droplet.ipv4_address
  ttl    = 300
}
