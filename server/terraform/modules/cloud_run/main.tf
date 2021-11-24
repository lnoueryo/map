resource "google_cloud_run_service" "default" {
  name     = var.name
  location = var.location

  metadata {
    annotations = {
        "run.googleapis.com/cloudsql-instances" = "trim-tide-313616:asia-northeast1:gmap"
    }
  }

  template {
    spec {
      service_account_name = "g-map-261@trim-tide-313616.iam.gserviceaccount.com"
      containers {
        image = "gcr.io/trim-tide-313616/map"
        env {
          name = "SECRET_ENV_VAR"
      value_from {
            secret_key_ref {
              name = "gmap-keys"
              key = "latest"
            }
          }
        }
      }
    }
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.default.location
  project     = google_cloud_run_service.default.project
  service     = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

resource "google_cloud_run_domain_mapping" "default" {
  location = google_cloud_run_service.default.location
  name     = "tap-map-practice.api.jounetsism.biz"

  metadata {
    namespace = var.project
  }

  spec {
    route_name = google_cloud_run_service.default.name
  }
}
