output "host" {
  description = "The private host of the PostgreSQL cluster"
  value       = digitalocean_database_cluster.postgres.private_host
}

output "port" {
  description = "The port of the PostgreSQL cluster"
  value       = digitalocean_database_cluster.postgres.port
}

output "litellm_connection_uri" {
  description = "The full PostgreSQL connection URI for the LiteLLM application"
  value       = "postgresql://${digitalocean_database_user.litellm.name}:${digitalocean_database_user.litellm.password}@${digitalocean_database_cluster.postgres.private_host}:${digitalocean_database_cluster.postgres.port}/${digitalocean_database_db.litellm.name}?sslmode=require"
  sensitive   = true
}

output "langfuse_connection_uri" {
  description = "The full PostgreSQL connection URI for the Langfuse application"
  value       = "postgresql://${digitalocean_database_user.langfuse.name}:${digitalocean_database_user.langfuse.password}@${digitalocean_database_cluster.postgres.private_host}:${digitalocean_database_cluster.postgres.port}/${digitalocean_database_db.langfuse.name}?sslmode=require"
  sensitive   = true
}
