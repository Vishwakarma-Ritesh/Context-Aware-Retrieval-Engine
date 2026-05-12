variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "artifact_bucket_name" {
  type        = string
  description = "Bucket used for benchmark exports or corpus snapshots."
}
