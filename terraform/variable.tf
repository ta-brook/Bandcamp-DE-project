locals {
    data_lake_bucket = "bandcamp_sale_data_lake"
}

variable "project" {
    description = "Your GCP Project ID"
}

variable "region" {
    description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
    default = "asia-southeast1"
    type = string
}

variable "storage_class" {
    description = "Storage class type for your bucket. Check official docs for more info."
    default = "STANDARD"
}

variable "BQ_DATASET" {
    description = "BigQuery Dataset that raw data (from GCS) will be written to"
    type = string
    default = "bandcamp_sale_all_data"
}

variable "BQ_DATASET_PROD" {
    description = "BigQuery Dataset that raw data (from GCS) will be written to (production)"
    type = string
    default = "bandcamp_sale_prod"
}

variable "machine_type" {
    description = "machine type that dataproc will created for you"
    type = string
    default = "n1-standard-2"
}
