
variable "cluster_name" {
  description = "The name of the Kubernetes cluster"
  type        = string
}

variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The region for the resources"
  type        = string
}