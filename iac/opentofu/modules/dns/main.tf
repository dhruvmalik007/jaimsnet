terraform {
  required_version = ">= 1.5.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
}

# 1. Manage the Domain Zone natively
resource "digitalocean_domain" "zone" {
  name = var.domain
}

# 2. Provision A and CNAME Records
resource "digitalocean_record" "routing" {
  count = length(var.records)

  domain = digitalocean_domain.zone.name
  type   = var.records[count.index].type
  name   = var.records[count.index].name
  # Automatically use lb_ip if value is specifically empty or "use_lb_ip"
  value = contains(["", "use_lb_ip"], var.records[count.index].value) ? var.lb_ip : var.records[count.index].value
  ttl   = 300
}

# 3. Provision TXT Records (FedArch compliance: SPF, DMARC, Verification)
resource "digitalocean_record" "txt" {
  for_each = var.txt_records

  domain = digitalocean_domain.zone.name
  type   = "TXT"
  # Standardize naming: _dmarc for DMARC, @ for SPF/verification in case of temporary naming.
  name  = try(regex("_dmarc", each.key) == "_dmarc" ? "_dmarc" : "@", "@")
  value = each.value
  ttl   = 3600
}
