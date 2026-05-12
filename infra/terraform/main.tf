terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "benchmark_artifacts" {
  bucket = var.artifact_bucket_name
}

resource "aws_cloudwatch_log_group" "service_logs" {
  name              = "/semantic-rag-engine/${var.environment}"
  retention_in_days = 14
}
