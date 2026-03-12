output "domain_name" {
  description = "The registered domain name"
  value       = digitalocean_domain.zone.name
}

output "domain_urn" {
  description = "The URN of the domain zone"
  value       = digitalocean_domain.zone.urn
}

output "routing_records" {
  description = "List of created A and CNAME record hostnames"
  value       = [for r in digitalocean_record.routing : r.fqdn]
}
