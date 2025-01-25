variable "bucket_name" {
  type = string
}

variable "project_id" {
  type = string
  default = "cartola-360814"
}


variable "region" {
  type = string
  default = "us-east1"
}


variable "service_account" {
  type = string
  default = "functions-cartola@cartola-360814.iam.gserviceaccount.com"
}


variable "config_file_path" {
  default = "config.json"
}
