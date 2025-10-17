# Variables for AWS EKS deployment

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "swen-ai-pipeline"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type for EKS nodes"
  type        = string
  default     = "t3.medium"
}

variable "min_nodes" {
  description = "Minimum number of nodes in EKS cluster"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum number of nodes in EKS cluster"
  type        = number
  default     = 5
}

variable "desired_nodes" {
  description = "Desired number of nodes in EKS cluster"
  type        = number
  default     = 3
}

# Database variables
variable "db_name" {
  description = "Database name"
  type        = string
  default     = "swen_news"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "swen_admin"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.micro"  # Free tier eligible for testing
  # For production, use: "db.t4g.medium" or larger
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS in GB"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for RDS autoscaling in GB"
  type        = number
  default     = 100
}

