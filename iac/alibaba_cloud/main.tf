# Terraform configuration for Alibaba Cloud ACK deployment
# SWEN AI-Enriched News Pipeline

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.210"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "alicloud" {
  region = var.alibaba_region
}

# VPC Configuration
resource "alicloud_vpc" "main" {
  vpc_name   = "${var.project_name}-vpc"
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# VSwitch (Subnet)
resource "alicloud_vswitch" "main" {
  count        = 3
  vpc_id       = alicloud_vpc.main.id
  cidr_block   = "10.0.${count.index + 1}.0/24"
  zone_id      = data.alicloud_zones.default.zones[count.index % length(data.alicloud_zones.default.zones)].id
  vswitch_name = "${var.project_name}-vswitch-${count.index + 1}"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Data source for availability zones
data "alicloud_zones" "default" {
  available_resource_creation = "VSwitch"
}

# ACK (Container Service for Kubernetes) Cluster
resource "alicloud_cs_managed_kubernetes" "main" {
  name                      = "${var.project_name}-cluster"
  cluster_spec              = var.cluster_spec
  worker_vswitch_ids        = alicloud_vswitch.main[*].id
  new_nat_gateway           = true
  pod_cidr                  = "172.20.0.0/16"
  service_cidr              = "172.21.0.0/20"
  slb_internet_enabled      = true
  
  # Add-ons
  addons {
    name = "terway-eniip"
  }
  addons {
    name = "csi-plugin"
  }
  addons {
    name = "csi-provisioner"
  }
  addons {
    name = "logtail-ds"
    config = jsonencode({
      "IngressDashboardEnabled" : "true"
    })
  }
  addons {
    name = "nginx-ingress-controller"
    config = jsonencode({
      "IngressSlbNetworkType" : "internet"
    })
  }
  addons {
    name = "arms-prometheus"
  }
  addons {
    name = "ack-node-problem-detector"
    config = jsonencode({
      "sls_project_name" : ""
    })
  }
}

# Node Pool
resource "alicloud_cs_kubernetes_node_pool" "main" {
  cluster_id     = alicloud_cs_managed_kubernetes.main.id
  node_pool_name = "${var.project_name}-node-pool"
  vswitch_ids    = alicloud_vswitch.main[*].id
  
  scaling_config {
    min_size = var.min_nodes
    max_size = var.max_nodes
  }
  
  instance_types       = [var.instance_type]
  system_disk_category = "cloud_efficiency"
  system_disk_size     = 120
  
  # Auto scaling
  scaling_policy = "release"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Container Registry
resource "alicloud_cr_namespace" "main" {
  name               = var.project_name
  auto_create        = true
  default_visibility = "PRIVATE"
}

resource "alicloud_cr_repo" "app" {
  namespace = alicloud_cr_namespace.main.name
  name      = "ai-pipeline"
  summary   = "SWEN AI-Enriched News Pipeline"
  repo_type = "PRIVATE"
}

# Security Group
resource "alicloud_security_group" "main" {
  name        = "${var.project_name}-sg"
  description = "Security group for SWEN AI Pipeline"
  vpc_id      = alicloud_vpc.main.id
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "alicloud_security_group_rule" "allow_http" {
  type              = "ingress"
  ip_protocol       = "tcp"
  policy            = "accept"
  port_range        = "80/80"
  security_group_id = alicloud_security_group.main.id
  cidr_ip           = "0.0.0.0/0"
}

resource "alicloud_security_group_rule" "allow_https" {
  type              = "ingress"
  ip_protocol       = "tcp"
  policy            = "accept"
  port_range        = "443/443"
  security_group_id = alicloud_security_group.main.id
  cidr_ip           = "0.0.0.0/0"
}

# Security Group for RDS
resource "alicloud_security_group_rule" "rds_from_cluster" {
  type              = "ingress"
  ip_protocol       = "tcp"
  policy            = "accept"
  port_range        = "5432/5432"
  security_group_id = alicloud_security_group.main.id
  cidr_ip           = "10.0.0.0/16"  # VPC CIDR
  description       = "PostgreSQL access from ACK cluster"
}

# Generate random password for RDS
resource "random_password" "db_password" {
  length  = 32
  special = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# RDS PostgreSQL Instance
resource "alicloud_db_instance" "postgres" {
  engine               = "PostgreSQL"
  engine_version       = "17.0"
  instance_type        = var.db_instance_class
  instance_storage     = var.db_allocated_storage
  instance_charge_type = "Postpaid"
  instance_name        = "${var.project_name}-postgres-${var.environment}"
  vswitch_id           = alicloud_vswitch.main[0].id
  security_ips         = ["10.0.0.0/16"]  # Allow access from VPC
  
  # High availability for production
  zone_id               = data.alicloud_zones.default.zones[0].id
  zone_id_slave_a       = var.environment == "production" ? data.alicloud_zones.default.zones[1].id : null
  instance_storage_type = "cloud_essd"
  
  # Backup configuration
  backup_retention_period = var.environment == "production" ? 30 : 7
  preferred_backup_time   = "02:00Z-03:00Z"
  preferred_backup_period = ["Monday", "Wednesday", "Friday"]
  
  # Monitoring
  monitoring_period = 60
  
  # Maintenance window
  maintenance_window = "Mon:04:00Z-Mon:05:00Z"
  
  # Auto-upgrade minor versions
  auto_upgrade_minor_version = "Auto"
  
  # Deletion protection
  deletion_protection = var.environment == "production"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Database account
resource "alicloud_db_account" "main" {
  db_instance_id = alicloud_db_instance.postgres.id
  account_name   = var.db_username
  account_password = random_password.db_password.result
  account_type     = "Super"
  account_description = "Main database account for SWEN AI Pipeline"
}

# Create database
resource "alicloud_db_database" "main" {
  instance_id = alicloud_db_instance.postgres.id
  name        = var.db_name
  character_set = "UTF8"
  description = "SWEN News database"
  
  depends_on = [alicloud_db_account.main]
}

# Store database credentials in KMS (Key Management Service)
resource "alicloud_kms_secret" "db_credentials" {
  secret_name = "${var.project_name}-db-credentials-${var.environment}"
  description = "Database credentials for SWEN AI Pipeline"
  
  secret_data = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    engine   = "postgres"
    host     = alicloud_db_instance.postgres.connection_string
    port     = 5432
    dbname   = var.db_name
    instance_id = alicloud_db_instance.postgres.id
  })
  
  version_stages = ["ACSCurrent"]
  force_delete_without_recovery = var.environment != "production"
  recovery_window_in_days = var.environment == "production" ? 30 : 7
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# RAM Role for ACK pods to access KMS secrets
resource "alicloud_ram_role" "kms_access" {
  name = "${var.project_name}-kms-access"
  description = "Role for ACK pods to access KMS secrets"
  document = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = ["ecs.aliyuncs.com"]
        }
      }
    ]
    Version = "1"
  })
  
  force = true
}

resource "alicloud_ram_policy" "kms_access" {
  policy_name = "${var.project_name}-kms-policy"
  description = "Policy for accessing KMS secrets"
  
  policy_document = jsonencode({
    Statement = [
      {
        Action = [
          "kms:GetSecretValue",
          "kms:DescribeSecret"
        ]
        Effect = "Allow"
        Resource = alicloud_kms_secret.db_credentials.arn
      }
    ]
    Version = "1"
  })
}

resource "alicloud_ram_role_policy_attachment" "kms_access" {
  policy_name = alicloud_ram_policy.kms_access.policy_name
  policy_type = "Custom"
  role_name   = alicloud_ram_role.kms_access.name
}

# Outputs
output "cluster_id" {
  description = "ACK cluster ID"
  value       = alicloud_cs_managed_kubernetes.main.id
}

output "cluster_name" {
  description = "ACK cluster name"
  value       = alicloud_cs_managed_kubernetes.main.name
}

output "kubeconfig" {
  description = "Kubeconfig for ACK cluster"
  value       = alicloud_cs_managed_kubernetes.main.kube_config
  sensitive   = true
}

output "registry_url" {
  description = "Container Registry URL"
  value       = "${alicloud_cr_namespace.main.name}.${var.alibaba_region}.cr.aliyuncs.com"
}

output "rds_connection_string" {
  description = "RDS PostgreSQL connection string"
  value       = alicloud_db_instance.postgres.connection_string
}

output "rds_port" {
  description = "RDS PostgreSQL port"
  value       = alicloud_db_instance.postgres.port
}

output "kms_secret_arn" {
  description = "ARN of the KMS secret containing database credentials"
  value       = alicloud_kms_secret.db_credentials.arn
}

output "database_url" {
  description = "Database connection URL (password stored in KMS)"
  value       = "postgresql+asyncpg://${var.db_username}:<password>@${alicloud_db_instance.postgres.connection_string}:5432/${var.db_name}"
  sensitive   = false
}

