
variable "ssh_key_name" {
  description = "Name of the SSH key on your DigitalOcean account to inject into the droplet"
  type        = string
}

variable "customer_id" {
  description = "Identifier for the customer / deployment (e.g. acme-inc)"
  type        = string
  default     = "lite-customer"
}

variable "region" {
  description = "DO Region slug"
  type        = string
  default     = "nyc3"
}

variable "droplet_size" {
  description = "Instance size"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "enable_watchtower" {
  description = "Whether to deploy Watchtower for automated container updates"
  type        = bool
  default     = false
}

variable "domain_name" {
  description = "DigitalOcean-managed domain name (e.g. weown.tools)"
  type        = string
  default     = ""
}

variable "allowed_ssh_cidrs" {
  description = "Explicit allowlist of CIDR blocks permitted to connect via SSH (Port 22). Must be set to your team/operator IPs — do NOT use 0.0.0.0/0 in any real deployment."
  type        = list(string)
  default     = [] # No default: force an explicit allowlist at deploy time

  validation {
    condition = alltrue([
      for cidr in var.allowed_ssh_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "All entries in allowed_ssh_cidrs must be valid CIDR notation (e.g. '203.0.113.0/24')."
  }
}

variable "allowed_api_cidrs" {
  description = "Explicit allowlist of CIDR blocks permitted to reach AI API endpoints (ports 3001, 11434, 4000). Defaults open for API access — restrict to known clients in production deployments."
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"] # API endpoints may legitimately be public, but review before deploying

  validation {
    condition = alltrue([
      for cidr in var.allowed_api_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "All entries in allowed_api_cidrs must be valid CIDR notation (e.g. '203.0.113.0/24')."
  }
}

variable "litellm_base_url" {
  description = "The centralized LiteLLM Gateway URL"
  type        = string
  default     = "https://litellm.jAIMS.app"
}

variable "litellm_api_key" {
  description = "The API key for the centralized LiteLLM Gateway"
  type        = string
  sensitive   = true
}
