output "vpc_id" {
  description = "The UUID of the Core VPC"
  value       = module.vpc.vpc_id
}

output "doks_cluster_id" {
  description = "The ID of the DOKS cluster"
  value       = module.doks.cluster_id
}

output "doks_cluster_kubeconfig" {
  description = "Kubeconfig content to access the cluster locally"
  value       = module.doks.kubeconfig
  sensitive   = true
}

output "db_litellm_uri" {
  description = "Secure internal connection URI for LiteLLM DB"
  value       = module.database.litellm_connection_uri
  sensitive   = true
}

output "db_langfuse_uri" {
  description = "Secure internal connection URI for Langfuse DB"
  value       = module.database.langfuse_connection_uri
  sensitive   = true
}

output "domain_name" {
  description = "The configured root domain (if applicable)"
  value       = var.domain != "" ? module.dns[0].domain_name : null
}

output "dns_records" {
  description = "The fully qualified domain names provisioned"
  value       = var.domain != "" ? module.dns[0].routing_records : []
}
