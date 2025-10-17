# AWS EKS Deployment

This directory contains Terraform configuration for deploying the SWEN AI-Enriched News Pipeline on AWS using EKS (Elastic Kubernetes Service).

## Resources Created

- **VPC**: Virtual Private Cloud with public and private subnets
- **EKS Cluster**: Managed Kubernetes cluster
- **ECR Repository**: Container registry for Docker images
- **Application Load Balancer**: For HTTP/HTTPS traffic
- **Security Groups**: Network security rules
- **Auto Scaling**: Managed node groups with auto-scaling

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform >= 1.0
3. kubectl for Kubernetes management

## Usage

### Initialize Terraform

```bash
terraform init
```

### Plan Deployment

```bash
terraform plan
```

### Apply Configuration

```bash
terraform apply
```

### Configure kubectl

```bash
aws eks update-kubeconfig --name swen-ai-pipeline-cluster --region us-east-1
```

### Deploy Application

```bash
# Build and push Docker image
docker build -t swen-ai-pipeline .
docker tag swen-ai-pipeline:latest <ECR_URL>/swen-ai-pipeline:latest
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ECR_URL>
docker push <ECR_URL>/swen-ai-pipeline:latest

# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## Variables

- `aws_region`: AWS region (default: us-east-1)
- `project_name`: Project name for resources
- `environment`: Environment name
- `instance_type`: EC2 instance type
- `min_nodes`: Minimum cluster nodes
- `max_nodes`: Maximum cluster nodes

## Outputs

- `cluster_endpoint`: EKS cluster API endpoint
- `cluster_name`: EKS cluster name
- `ecr_repository_url`: ECR repository URL
- `load_balancer_dns`: Load balancer DNS name

## Cleanup

```bash
terraform destroy
```

