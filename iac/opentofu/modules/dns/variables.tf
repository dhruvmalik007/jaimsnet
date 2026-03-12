variable "domain" {
  type        = string
  description = "The root domain name (e.g., jaims.app)"
}

variable "lb_ip" {
  type        = string
  description = "The DigitalOcean Load Balancer IP for A records routing"
}

variable "records" {
  type = list(object({
    name  = string
    type  = string
    value = string
  }))
  description = "List of DNS records to create for hosting the applications. If 'value' is empty or 'use_lb_ip', the lb_ip will be used."
  default     = []
}

variable "txt_records" {
  type        = map(string)
  description = "TXT records for SPF, DMARC, and Domain Verification."
  default     = {}
}
