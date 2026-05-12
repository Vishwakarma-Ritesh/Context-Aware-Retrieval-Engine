output "artifact_bucket_name" {
  value = aws_s3_bucket.benchmark_artifacts.bucket
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.service_logs.name
}
