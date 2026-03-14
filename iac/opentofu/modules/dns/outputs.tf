output "domain_name" {
  description = "The domain name managed or referenced by this module"
  value       = local.domain_name
}

output "is_imported" {
  description = "Whether the domain was imported"
  value       = var.import_existing_domain
}

output "droplet_records" {
  description = "List of created droplet DNS records"
  value       = [for r in digitalocean_record.droplet_records : r.fqdn]
}

output "doks_records" {
  description = "List of created DOKS DNS records"
  value       = [for r in digitalocean_record.doks_records : r.fqdn]
}
