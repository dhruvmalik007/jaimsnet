output "lb_ip" {
  description = "The public IP of the Load Balancer"
  value       = digitalocean_loadbalancer.lb.ip
}

output "lb_id" {
  description = "The ID of the Load Balancer"
  value       = digitalocean_loadbalancer.lb.id
}
