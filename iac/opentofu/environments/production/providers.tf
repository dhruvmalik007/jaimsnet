terraform {
  required_version = ">= 1.5.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }
}

provider "digitalocean" {

}

# The DOKS cluster is dynamic, so we configure the K8s and Helm providers to use its attributes.
# Warning: During the initial apply, Terraform might struggle if the cluster isn't created yet 
# due to provider initialization phases, but OpenTofu/Terraform 1.x handles this much better.
provider "kubernetes" {
  host  = module.doks.cluster_endpoint
  token = module.doks.kubeconfig_token
  cluster_ca_certificate = base64decode(
    module.doks.kubeconfig_ca
  )
}

provider "helm" {
  kubernetes {
    host  = module.doks.cluster_endpoint
    token = module.doks.kubeconfig_token
    cluster_ca_certificate = base64decode(
      module.doks.kubeconfig_ca
    )
  }
}
