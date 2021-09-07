# https://console.cloud.google.com/monitoring/alerting/notifications?hl=ja&project=trim-tide-313616
resource "google_monitoring_notification_channel" "basic" {
  display_name = "Map Notification Channel"
  type = "email"
  labels = {
    email_address = var.notification_email_address
  }
}
# https://console.cloud.google.com/monitoring/uptime?hl=ja&project=trim-tide-313616
resource "google_monitoring_uptime_check_config" "https" {
  display_name = "https-uptime-check"
  timeout      = "60s"
  period       = "60s"
  http_check {
    path = "/"
    port = "443"
    use_ssl = true
    validate_ssl = true
    request_method = "GET"
  }
  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = var.host_name
    }
  }
}
# https://console.cloud.google.com/monitoring/alerting?hl=ja&project=storelocator-v2
resource "google_monitoring_alert_policy" "map_alert_policy" {
  display_name = "map"
  combiner = "OR"
  enabled = true
  conditions {
    display_name = "Failure of uptime check_id map"
    condition_threshold {
      filter = "metric.type=\"monitoring.googleapis.com/uptime_check/check_passed\" resource.type=\"uptime_url\" metric.label.\"check_id\"=\"${google_monitoring_uptime_check_config.https.name}\""
      comparison = "COMPARISON_GT"
      threshold_value = 1
      duration = "300s"
      trigger {
        percent = 100
      }
      aggregations {
        alignment_period = "1200s"
        per_series_aligner = "ALIGN_NEXT_OLDER"
        cross_series_reducer = "REDUCE_COUNT_FALSE"
        group_by_fields = ["resource.label.*"]
      }
    }
  }
  notification_channels = [google_monitoring_notification_channel.basic.name]
}