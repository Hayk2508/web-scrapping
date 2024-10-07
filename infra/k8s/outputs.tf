output "cluster_name" {
  description = "The name of the Kubernetes cluster"
  value       = google_container_cluster.web_cluster.name
}

output "cluster_endpoint" {
  description = "The endpoint of the Kubernetes cluster"
  value       = google_container_cluster.web_cluster.endpoint
}