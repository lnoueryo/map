provider "google" {
  credentials  = "${file("${var.credentials}")}"
  project      = "${var.project}"
  region       = "${var.region}"
}

resource "google_sql_database_instance" "master" {
  name = "gmap"
  database_version = "MYSQL_5_7"
  region       = "${var.region}"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name      = "tap-map"
  instance  = "${google_sql_database_instance.master.name}"
  charset   = "sjis"
  collation = "sjis_japanese_ci"
}

resource "google_sql_user" "users" {
  name     = "admin"
  instance = "${google_sql_database_instance.master.name}"
  host     = "%"
  password = "admin"
}