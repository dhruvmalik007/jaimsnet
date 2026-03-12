output "id" {
  description = "The ID of the droplet"
  value       = module.lite_droplet.droplet_id
}

output "ipv4_address" {
  description = "The public IPv4 address of the droplet"
  value       = module.lite_droplet.ipv4_address
}

output "ssh_command" {
  description = "The command used to SSH into the instance"
  value       = "ssh ubuntu@${module.lite_droplet.ipv4_address}"
}

output "anythingllm_url" {
  description = "The URL to access AnythingLLM"
  value       = var.domain_name != "" ? "https://${var.customer_id}.${var.domain_name}" : "http://${module.lite_droplet.ipv4_address}:3001"
}
