output "droplet_id" {
  description = "The ID of the droplet"
  value       = digitalocean_droplet.anythingllm.id
}

output "ipv4_address" {
  description = "The public IPv4 address of the droplet"
  value       = digitalocean_droplet.anythingllm.ipv4_address
}

output "ssh_command" {
  description = "The command used to SSH into the instance"
  value       = "ssh root@${digitalocean_droplet.anythingllm.ipv4_address}"
}

output "dns_record_fqdn" {
  description = "The fully qualified domain name of the DNS A record (if any)"
  value       = var.domain_name != "" ? digitalocean_record.anythingllm_a_record[0].fqdn : ""
}

output "anythingllm_url" {
  description = "The HTTP/HTTPS URL to access AnythingLLM"
  value       = var.domain_name != "" ? "https://${digitalocean_record.anythingllm_a_record[0].fqdn}" : "http://${digitalocean_droplet.anythingllm.ipv4_address}:3001"
}
