
terraform {
  backend "gcs" {
    bucket = "gcp-finance"
    prefix = "function"
  }
}
