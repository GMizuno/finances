output "cloud_scheduler_body" {
  value = base64decode(google_cloud_scheduler_job.invoke_cloud_function.http_target[0].body)
}

output "cloud_scheduler_schedule" {
  value = google_cloud_scheduler_job.invoke_cloud_function.schedule
}



