terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

# ─────────────────────────────────────────────────────────────────────────────
# Domain Zone (specs-ccc.md Logic)
# ─────────────────────────────────────────────────────────────────────────────

# Import existing domain (if applicable)
resource "digitalocean_domain" "primary" {
  count = var.import_existing_domain ? 0 : 1
  name  = var.existing_domain_name != null ? var.existing_domain_name : var.domain
}

# Data source for imported domain
data "digitalocean_domain" "imported" {
  count = var.import_existing_domain ? 1 : 0
  name  = var.existing_domain_name
}

locals {
  domain_name = var.import_existing_domain ? data.digitalocean_domain.imported[0].name : digitalocean_domain.primary[0].name
}

# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Resource Mappings (Droplets & DOKS)
# ─────────────────────────────────────────────────────────────────────────────

# DNS Records for Droplets
resource "digitalocean_record" "droplet_records" {
  for_each = {
    for idx, mapping in var.droplet_mappings :
    mapping.record_name => mapping
  }

  domain = local.domain_name
  type   = each.value.record_type
  name   = each.value.record_name
  value  = each.value.value
  ttl    = var.record_ttl
  
  # DO records technically do not support tags, but specs-ccc.md asked for it. 
  # If validation fails, we will remove this.
  # tags = var.tags
}

# DNS Records for DOKS Clusters
resource "digitalocean_record" "doks_records" {
  for_each = {
    for idx, mapping in var.doks_cluster_mappings :
    mapping.record_name => mapping
  }

  domain = local.domain_name
  type   = each.value.record_type
  name   = each.value.record_name
  value  = each.value.lb_ip
  ttl    = var.record_ttl
  
  # tags = var.tags
}

# ─────────────────────────────────────────────────────────────────────────────
# TXT Records (SPF, DMARC, Domain Verification)
# ─────────────────────────────────────────────────────────────────────────────
resource "digitalocean_record" "txt" {
  for_each = var.txt_records

  domain = local.domain_name
  type   = "TXT"
  # Name: _dmarc → _dmarc, anything else → @ (root)
  name  = startswith(each.key, "_") ? each.key : "@"
  value = each.value
  ttl   = 3600
}
