output "cluster_id" {
  description = "The ID of the DOKS cluster"
  value       = digitalocean_kubernetes_cluster.cluster.id
}

output "cluster_endpoint" {
  description = "The URL of the API server for the cluster"
  value       = digitalocean_kubernetes_cluster.cluster.endpoint
}

output "kubeconfig" {
  description = "The raw kubeconfig string for accessing the cluster locally"
  value       = digitalocean_kubernetes_cluster.cluster.kube_config[0].raw_config
  sensitive   = true
}

output "kubeconfig_token" {
  description = "The raw token for accessing the cluster server from the DO provider"
  value       = digitalocean_kubernetes_cluster.cluster.kube_config[0].token
  sensitive   = true
}

output "kubeconfig_ca" {
  description = "The raw CA cert string for accessing the cluster from the DO provider"
  value       = digitalocean_kubernetes_cluster.cluster.kube_config[0].cluster_ca_certificate
  sensitive   = true
}
