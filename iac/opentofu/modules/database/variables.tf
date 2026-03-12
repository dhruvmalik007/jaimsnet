variable "cluster_name" {
  type        = string
  description = "Name for the Managed PostgreSQL database cluster"
}

variable "region" {
  type        = string
  description = "DigitalOcean region slug"
}

variable "size" {
  type        = string
  description = "Droplet size slug for the database nodes"
}

variable "node_count" {
  type        = number
  description = "Number of database nodes (1 for primary only, >1 for standby)"
  default     = 1
}

variable "vpc_uuid" {
  type        = string
  description = "VPC UUID to attach the database cluster"
}
