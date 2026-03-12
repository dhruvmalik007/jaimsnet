variable "cluster_name" {
  type        = string
  description = "The name of the DOKS cluster"
}

variable "region" {
  type        = string
  description = "The DigitalOcean region for the cluster"
}

variable "k8s_version" {
  type        = string
  description = "The slug for the Kubernetes version to use"
}

variable "node_size" {
  type        = string
  description = "The Droplet size for the worker nodes (e.g., s-4vcpu-8gb)"
}

variable "node_min_count" {
  type        = number
  description = "The minimum number of nodes in the auto-scaling worker pool"
  default     = 2
}

variable "node_max_count" {
  type        = number
  description = "The maximum number of nodes in the auto-scaling worker pool"
  default     = 5
}

variable "vpc_uuid" {
  type        = string
  description = "The UUID of the VPC to deploy the cluster into"
}

variable "tags" {
  type        = list(string)
  description = "A list of tags to apply to the cluster and node pool"
  default     = []
}
