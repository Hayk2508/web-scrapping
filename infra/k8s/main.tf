provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "web_cluster" {
  name     = var.cluster_name
  location = var.region

  enable_autopilot = true
}
