# Variables for Alibaba Cloud ACK deployment

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

variable "alibaba_region" {
  description = "Alibaba Cloud region for resources"
  type        = string
  default     = "cn-hangzhou"
}

variable "cluster_spec" {
  description = "ACK cluster specification"
  type        = string
  default     = "ack.pro.small"
}

variable "instance_type" {
  description = "ECS instance type for ACK nodes"
  type        = string
  default     = "ecs.c6.large"
}

variable "min_nodes" {
  description = "Minimum number of nodes in ACK cluster"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum number of nodes in ACK cluster"
  type        = number
  default     = 5
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
  default     = "pg.n2.small.1"  # Entry-level PostgreSQL instance
  # For production, use: "pg.n4.medium.1" or larger
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS in GB"
  type        = number
  default     = 20
}

