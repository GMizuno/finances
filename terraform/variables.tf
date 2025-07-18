variable "bucket_name" {
  type = string
}

variable "project_id" {
  type    = string
  default = "cartola-360814"
}


variable "region" {
  type    = string
  default = "us-east1"
}


variable "service_account" {
  type    = string
  default = "functions-cartola@cartola-360814.iam.gserviceaccount.com"
}


variable "config_file_path" {
  type    = string
  default = "config.json"
}

variable "cron" {
  type = string
}

variable "time_zone" {
  type    = string
  default = "America/Sao_Paulo"
}

variable "repository" {
  type    = string
  default = "gcf-artifacts"
}
