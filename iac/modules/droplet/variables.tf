variable "ssh_key_name" {
  description = "Name of the existing SSH key in DigitalOcean"
  type        = string
}

variable "droplet_name" {
  description = "Base name for the droplet (e.g. allm-acme)"
  type        = string
  default     = "anythingllm-lite"
}

variable "region" {
  description = "DigitalOcean region slug"
  type        = string
  default     = "atl1"
}

variable "droplet_size" {
  description = "Droplet size (minimum 2GB RAM / 1 vCPU recommended for AnythingLLM)"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "vpc_uuid" {
  description = "VPC UUID to deploy the droplet into (optional)"
  type        = string
  default     = ""
}

variable "enable_watchtower" {
  description = "Enable Watchtower for automatic tracking and deployment of the container. If false, it's ignored."
  type        = bool
  default     = false
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

variable "domain_name" {
  description = "The DigitalOcean-managed domain name to attach to this instance (e.g. weown.tools)"
  type        = string
  default     = ""
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
