data "google_project" "project" {
}
resource "google_secret_manager_secret" "secret-basic" {
  secret_id = var.secret_id

  labels = {
    label = "my-label"
  }

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret-version-basic" {
  secret = google_secret_manager_secret.secret-basic.id

  secret_data = var.secret_data
}

resource "google_secret_manager_secret_iam_member" "secret-access" {

  secret_id = google_secret_manager_secret.secret-basic.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_secret_manager_secret.secret-basic]
}