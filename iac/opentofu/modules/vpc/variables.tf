variable "name" {
  type        = string
  description = "The name of the VPC"
}

variable "region" {
  type        = string
  description = "The region to provision the VPC in"
}

variable "ip_range" {
  type        = string
  description = "The CIDR block for the VPC"
  
  validation {
    condition     = can(cidrnetmask(var.ip_range))
    error_message = "The ip_range must be a valid CIDR block."
  }
}
