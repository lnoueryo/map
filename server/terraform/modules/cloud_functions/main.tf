resource "google_pubsub_topic" "instance_management" {
  name = "instance-management"
}

resource "google_cloud_scheduler_job" "job" {
  name        = "sql-instance"
  description = "sql-instance"
  schedule    = "0 12 * * 1-5"
  time_zone   = "Asia/Tokyo"

  pubsub_target {
    # topic.id is the topic's full resource name.
    topic_name = google_pubsub_topic.instance_management.id
    data       = base64encode("test")
  }
}
resource "google_storage_bucket" "functions_bucket" {
  name     = "trim-tide-313616"
  location = "asia-northeast1"
}

resource "google_storage_bucket_object" "functions_packages" {
  name   = "app/functions-${formatdate("YYYYMMDD-hhmm", timestamp())}.zip"
  bucket = "${google_storage_bucket.functions_bucket.name}"
  source = "../src/functions.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "start-or-stop-cloud-sql-instance"
  description = "start-or-stop-cloud-sql"
  runtime     = "python39"

  available_memory_mb   = 128
  source_archive_bucket = "${google_storage_bucket.functions_bucket.name}"
  source_archive_object = "${google_storage_bucket_object.functions_packages.name}"
  timeout               = 60
  entry_point           = "check_time"
  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.instance_management.name
  }
}