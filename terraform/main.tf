data "local_file" "config" {
  filename = var.config_file_path
}

locals {
  config = jsondecode(data.local_file.config.content)
}

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
      "pyproject.toml",
      ".git",
      ".github",
      ".gitignore",
      "*.json",
      "README.md"
    ])
  )
}

resource "google_storage_bucket_object" "source_zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "source_zip-${data.archive_file.source.output_md5}.zip"
  bucket       = var.bucket_name
}


resource "google_cloudfunctions2_function" "cloud_functions" {
  name        = "finance"
  description = "Cloud-function to extract data from Yahoo Finance"
  project     = var.project_id
  location    = var.region

  build_config {
    runtime           = "python310"
    entry_point       = "main"
    docker_repository = "projects/${var.project_id}/locations/${var.region}/repositories/${var.repository}"
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
    environment_variables = {
      LOG_EXECUTION_ID = "true"
    }
  }

}

resource "google_cloud_scheduler_job" "invoke_cloud_function" {
  name        = "invoke-function-finance"
  description = "Schedule the HTTPS trigger for cloud function"
  schedule    = var.cron
  time_zone   = var.time_zone
  project     = google_cloudfunctions2_function.cloud_functions.project
  region      = google_cloudfunctions2_function.cloud_functions.location

  http_target {
    uri         = "https://${var.region}-${var.project_id}.cloudfunctions.net/${google_cloudfunctions2_function.cloud_functions.name}"
    http_method = "POST"
    headers = {
      "Content-Type" = "application/json"
    }
    body = base64encode(jsonencode(local.config))
    oidc_token {
      audience              = "https://${var.region}-${var.project_id}.cloudfunctions.net/${google_cloudfunctions2_function.cloud_functions.name}"
      service_account_email = var.service_account
    }
  }
}


