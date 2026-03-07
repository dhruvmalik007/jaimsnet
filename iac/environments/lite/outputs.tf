output "id" {
  description = "The ID of the droplet"
  value       = module.lite_droplet.id
}

output "ipv4_address" {
  description = "The public IPv4 address of the droplet"
  value       = module.lite_droplet.ipv4_address
}

output "ssh_command" {
  description = "The command used to SSH into the instance"
  value       = module.lite_droplet.ssh_command
}

output "anythingllm_url" {
  description = "The URL to access AnythingLLM"
  value       = module.lite_droplet.anythingllm_url
}
