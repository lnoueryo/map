resource "google_project" "default" {
  provider = google-beta
  project_id = var.project_id
  name       = var.name
}

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = google_project.default.project_id
}

resource "google_firebase_project_location" "basic" {
    provider = google-beta
    project = google_firebase_project.default.project

    location_id = "asia-northeast1"
}
resource "google_firebase_web_app" "basic" {
    provider = google-beta
    project = google_project.default.project_id
    display_name = "tap-map"

    depends_on = [google_firebase_project.default]
}

data "google_firebase_web_app_config" "basic" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.basic.app_id
}
