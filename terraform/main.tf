terraform {
    required_version = ">= 1.0"
    backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
    required_providers {
        google = {
            source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
    name          = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
    location      = var.region

    # Optional, but recommended settings:
    storage_class = var.storage_class
    uniform_bucket_level_access = true

    versioning {
    enabled     = true
  }

    lifecycle_rule {
        action {
            type = "Delete"
    }
        condition {
            age = 30  // days
    }
  }

    force_destroy = true
}

# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET
    project    = var.project
    location   = var.region
}

resource "google_bigquery_dataset" "dataset_prod" {
    dataset_id = var.BQ_DATASET_PROD
    project    = var.project
    location   = var.region
}

# resource "google_dataproc_cluster" "bandcamp-cluster" {
#   name     = "bandcamp-cluster"
#   region   = var.region
#   graceful_decommission_timeout = "120s"

#  cluster_config {
#     staging_bucket = "dataproc-staging-bucket"
#     gce_cluster_config {
#       zone = "${var.region}-b"
#     }
    

#     master_config {
#       num_instances = 1
#       machine_type  = var.machine_type
#       disk_config {
#         boot_disk_type    = "pd-standard"
#         boot_disk_size_gb = 30
#       }
#     }

#     worker_config {
#       num_instances    = 2
#       machine_type     = var.machine_type
#       disk_config {
#         boot_disk_size_gb = 30
#       }
#     }
  # }
# }
