variable "name" {
  type        = string
  description = "Droplet name"
}

variable "region" {
  type        = string
  description = "DigitalOcean region"
}

variable "size" {
  type        = string
  description = "Droplet size slug"
  default     = "s-2vcpu-4gb"
}

variable "image" {
  type        = string
  description = "OS image (e.g., ubuntu-24-04-x64)"
  default     = "ubuntu-24-04-x64"
}

variable "ssh_key_ids" {
  type        = list(string)
  description = "SSH key IDs for access"
}

variable "vpc_uuid" {
  type        = string
  description = "VPC attachment"
  default     = ""
}

variable "tags" {
  type        = list(string)
  description = "Resource tags"
  default     = []
}

variable "user_data" {
  type        = string
  description = "Cloud-init script (optional)"
  default     = ""
}
