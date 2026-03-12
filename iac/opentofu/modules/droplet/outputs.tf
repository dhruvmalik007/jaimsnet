output "droplet_id" {
  description = "The ID of the droplet"
  value       = digitalocean_droplet.this.id
}

output "ipv4_address" {
  description = "The public IPv4 address of the droplet"
  value       = digitalocean_droplet.this.ipv4_address
}

output "ipv4_address_private" {
  description = "The private IPv4 address of the droplet within the VPC"
  value       = digitalocean_droplet.this.ipv4_address_private
}
