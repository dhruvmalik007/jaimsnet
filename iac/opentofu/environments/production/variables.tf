

variable "ssh_key_name" {
  description = "Name of the existing SSH key in DigitalOcean"
  type        = string
}

variable "region" {
  type        = string
  description = "DigitalOcean region slug"
  default     = "nyc3"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., core, prod, dev)"
  default     = "core"
}

variable "db_cluster_size" {
  type        = string
  description = "Droplet size for the database cluster"
  default     = "db-s-1vcpu-1gb"
}

variable "doks_cluster_version" {
  type        = string
  description = "Kubernetes version for DOKS (can be 'latest' or a specific version slug like '1.30.2-do.0')"
  default     = "latest"
}

variable "doks_node_size" {
  type        = string
  description = "Droplet size for DOKS worker nodes"
  default     = "s-4vcpu-8gb" # Sufficient for AI gateway services
}

variable "doks_min_nodes" {
  type        = number
  description = "Minimum number of worker nodes"
  default     = 2
}

variable "doks_max_nodes" {
  type        = number
  description = "Maximum number of worker nodes"
  default     = 5
}

variable "domain" {
  type        = string
  description = "The root domain name (e.g., jaims.app) to configure DNS for. If empty, DNS provisioning is skipped."
  default     = ""
}

variable "kuma_ip" {
  type        = string
  description = "The IP address of the Uptime Kuma instance. If set, an A record will be created for kuma."
  default     = ""
}

variable "allowed_ssh_cidrs" {
  type        = list(string)
  description = "List of allowed IPv4/IPv6 CIDR blocks for SSH access to the architecture (e.g. Uptime Kuma)."
  default     = ["0.0.0.0/0", "::/0"]
}
