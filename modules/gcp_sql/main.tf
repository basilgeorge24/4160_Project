provider "google" {
  credentials = file("C:\\csi4160-416400-ad90e57a9228.json")
  project     = "csi4160-416400"
  region      = "us-central1"
}

resource "google_compute_network" "vpc_network" {
  name = "default-vpc-network-for-project"
}
resource "google_compute_subnetwork" "subnet_region1" {
  name          = "subnet-region1-project"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.name
  ip_cidr_range = "10.1.0.0/24"
}

resource "google_sql_database_instance" "database_instance" {
  name              = "trial-database-instance-for-project"
  database_version  = "MYSQL_8_0"
  region            = "us-central1"
  project           = "csi4160-416400"

  settings {
    tier = "db-f1-micro"
  }

  deletion_protection = false
}
