output "vpc_id" {
  description = "The UUID of the VPC"
  value       = digitalocean_vpc.vpc.id
}

output "vpc_urn" {
  description = "The URN of the VPC"
  value       = digitalocean_vpc.vpc.urn
}

output "ip_range" {
  description = "The allocated CIDR block of the VPC"
  value       = digitalocean_vpc.vpc.ip_range
}
