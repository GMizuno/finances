data "archive_file" "source" {
  type        = "zip"
  source_dir = ".."  # Referência ao diretório pai (onde estão os arquivos principais, como main.py)
  output_path = "${path.module}/source/function_finance.zip"
  excludes = concat(
    tolist([
      # Exclusões explícitas de arquivos e pastas fora do diretório terraform
      ".terraform.lock.hcl", # Exclui o arquivo de lock do Terraform
      "terraform/*", # Exclui todos os arquivos na pasta terraform fora do diretório terraform
      "../terraform.tfstate", # Exclui o estado do Terraform
      "../terraform.tfstate.backup",
      "../venv", # Exclui a pasta venv fora do diretório terraform
      "../venv/*", # Exclui todos os arquivos dentro de venv
      ".idea", # Exclui a pasta .idea fora do diretório terraform
      ".gcloudignore", # Exclui o arquivo .gcloudignore fora do diretório terraform
      "poetry.lock",
      "pyproject.toml"
    ])
  )
}

data "local_file" "config" {
  filename = var.config_file_path
}

locals {
  config = jsondecode(data.local_file.config.content)
}

resource "google_storage_bucket_object" "source_zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "source_zip-${data.archive_file.source.output_md5}.zip"
  bucket       = var.bucket_name
}

resource "google_cloudfunctions2_function" "cloud_functions" {
  name        = "finance"
  description = "Cloud-function will get trigger once file is uploaded in input-${var.project_id}"
  project     = var.project_id
  location    = var.region

  build_config {
    runtime     = "python310"
    entry_point = "main"
    source {
      storage_source {
        bucket = var.bucket_name
        object = google_storage_bucket_object.source_zip.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "512M"
    timeout_seconds       = 60
    service_account_email = var.service_account
  }

}

resource "google_project_iam_binding" "cloud_function_invoker" {
  role = "roles/cloudfunctions.invoker"
  members = [
    "serviceAccount:${var.service_account}"
  ]
  project = var.project_id
}

resource "google_cloud_scheduler_job" "invoke_cloud_function" {
  name        = "invoke-function-finance"
  description = "Schedule the HTTPS trigger for cloud function"
  schedule    = "0 19 * * *"
  time_zone   = "America/Sao_Paulo"
  project     = google_cloudfunctions2_function.cloud_functions.project
  region      = google_cloudfunctions2_function.cloud_functions.location

  http_target {
    uri         = "https://us-east1-cartola-360814.cloudfunctions.net/finance"
    http_method = "POST"
    headers = {
      "Content-Type" = "application/json"
    }
    body = base64encode(jsonencode(local.config))
    oidc_token {
      audience              = "https://us-east1-cartola-360814.cloudfunctions.net/finance"
      service_account_email = var.service_account
    }
  }
}


