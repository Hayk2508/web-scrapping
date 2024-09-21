variable "project_id" {
  description = "The ID of the GCP project."
  type        = string
}

variable "region" {
  description = "The region where the GKE cluster will be created."
  type        = string
}

variable "cluster_name" {
  description = "The name of the GKE cluster."
  type        = string
}
