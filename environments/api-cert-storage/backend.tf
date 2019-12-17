terraform {
  backend "remote" {
    organization = "loci"
    workspaces {
      name = "dev-cert-store"
    }
  }
}

