variable "domain" {
  type        = string
  description = "The root domain name (e.g., jaims.app)."
  default     = ""
}

variable "import_existing_domain" {
  description = "Whether to import an existing domain (not registered via DO)"
  type        = bool
  default     = false
}

variable "existing_domain_name" {
  description = "Existing domain name to import (e.g., custom-domain.com)"
  type        = string
  default     = null
}

variable "custom_nameservers" {
  description = "Custom nameservers for domain delegation"
  type        = list(string)
  default     = ["ns1.digitalocean.com", "ns2.digitalocean.com", "ns3.digitalocean.com"]
}

variable "droplet_mappings" {
  description = "Map Droplet IDs to DNS records"
  type        = list(object({
    droplet_id  = string
    record_name = string
    record_type = string
    value       = string
  }))
  default = []
}

variable "doks_cluster_mappings" {
  description = "Map DOKS cluster IDs to DNS records"
  type        = list(object({
    cluster_id  = string
    record_name = string
    record_type = string
    lb_ip       = string
  }))
  default = []
}

variable "tags" {
  description = "Tags to apply to DNS records (if supported)"
  type        = list(string)
  default     = []
}

variable "txt_records" {
  type        = map(string)
  description = "TXT records for SPF, DMARC, and Domain Verification."
  default     = {}
}

variable "record_ttl" {
  type        = number
  description = "TTL in seconds for A and CNAME records."
  default     = 300
}
