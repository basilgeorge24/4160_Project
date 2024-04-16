provider "google" {
  credentials = file("C:\\csi4160-416400-ad90e57a9228.json")
  project     = "csi4160-416400"
  region      = "us-central1"
}

resource "google_compute_instance" "example_instance" {
  name         = "example-instance-for-project"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }
  network_interface {
    network = "default"
  }
}
