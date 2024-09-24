resource "google_kms_key_ring" "default" {
  name     = var.ring_name
  location = var.ring_location
}

resource "google_kms_crypto_key" "asymmetric_key" {
  name     = var.key_name
  key_ring = google_kms_key_ring.default.id

  purpose = "ASYMMETRIC_SIGN"

  version_template {
    algorithm = "RSA_SIGN_PSS_2048_SHA256"
    protection_level = "SOFTWARE"
  }
}


output "keyring" {
  value = google_kms_key_ring.default
}

output "asymmetric_key" {
  value = google_kms_crypto_key.asymmetric_key
}

