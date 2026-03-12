variable "name" {
  type        = string
  description = "The name of the Load Balancer"
}

variable "region" {
  type        = string
  description = "DigitalOcean region slug"
}

variable "vpc_uuid" {
  type        = string
  description = "VPC ID where the Load Balancer will be provisioned"
}

variable "ip" {
  type        = string
  description = "The reserved IP address to attach to the load balancer"
  default     = "129.212.240.75"
}

variable "doks_cluster_id" {
  type        = string
  description = "The ID of the DOKS cluster to dynamically fetch node droplet IDs"
}

variable "http_node_port" {
  type        = number
  description = "The NodePort used by the DOKS ingress-nginx service for HTTP"
  default     = 30080
}

variable "https_node_port" {
  type        = number
  description = "The NodePort used by the DOKS ingress-nginx service for HTTPS"
  default     = 30443
}
