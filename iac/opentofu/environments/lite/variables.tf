
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
  description = "List of CIDR blocks allowed to connect via SSH (Port 22)"
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}

variable "allowed_api_cidrs" {
  description = "List of CIDR blocks allowed to connect to AI API endpoints (3001, 11434, 4000)"
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
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
