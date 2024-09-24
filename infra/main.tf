provider "google" {
  project = var.project_id
  region  = var.region
}


module "k8s" {
  source = "./k8s"
  cluster_name = var.cluster_name
  project_id = var.project_id
  region = var.region
}

module "kms" {
  source = "./kms"
  ring_location = var.ring_location
  ring_name = var.ring_name
  key_name = var.key_name
}