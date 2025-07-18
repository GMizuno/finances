output "cloud_scheduler_body" {
  value = base64decode(google_cloud_scheduler_job.invoke_cloud_function.http_target[0].body)
}

output "cloud_scheduler_schedule" {
  value = google_cloud_scheduler_job.invoke_cloud_function.schedule
}

output "cloud_scheduler_uri" {
  value = google_cloudfunctions2_function.cloud_functions.service_config[0].uri
}


output "cloud_function_name" {
  value = google_cloudfunctions2_function.cloud_functions.name
}

output "project_id_from_data" {
  value = var.project_id
}

