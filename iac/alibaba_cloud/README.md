# Alibaba Cloud ACK Deployment

This directory contains Terraform configuration for deploying the SWEN AI-Enriched News Pipeline on Alibaba Cloud using ACK (Alibaba Cloud Container Service for Kubernetes).

## Resources Created

- **VPC**: Virtual Private Cloud
- **VSwitches**: Multiple subnets across availability zones
- **ACK Cluster**: Managed Kubernetes cluster
- **Container Registry**: Private Docker image registry
- **Node Pool**: Auto-scaling worker nodes
- **Security Groups**: Network security rules
- **Load Balancer**: Automatically created by ACK

## Prerequisites

1. Alibaba Cloud account with appropriate credentials
2. Terraform >= 1.0
3. kubectl for Kubernetes management

## Configuration

Set up your Alibaba Cloud credentials:

```bash
export ALICLOUD_ACCESS_KEY="your-access-key"
export ALICLOUD_SECRET_KEY="your-secret-key"
```

Or use the Alibaba Cloud CLI:

```bash
aliyun configure
```

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
# Get kubeconfig
terraform output -raw kubeconfig > kubeconfig.yaml
export KUBECONFIG=$(pwd)/kubeconfig.yaml

# Verify connection
kubectl get nodes
```

### Deploy Application

```bash
# Build and push Docker image
docker build -t swen-ai-pipeline .
docker tag swen-ai-pipeline:latest <REGISTRY_URL>/ai-pipeline:latest

# Login to Alibaba Container Registry
docker login --username=<your-username> <REGISTRY_URL>

docker push <REGISTRY_URL>/ai-pipeline:latest

# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## Variables

- `alibaba_region`: Alibaba Cloud region (default: cn-hangzhou)
- `project_name`: Project name for resources
- `environment`: Environment name
- `cluster_spec`: ACK cluster specification
- `instance_type`: ECS instance type
- `min_nodes`: Minimum cluster nodes
- `max_nodes`: Maximum cluster nodes

## Outputs

- `cluster_id`: ACK cluster ID
- `cluster_name`: ACK cluster name
- `kubeconfig`: Kubernetes configuration (sensitive)
- `registry_url`: Container Registry URL

## Cloud-Native Features

This configuration includes:
- **Auto-scaling**: Automatic node scaling based on demand
- **Load Balancing**: Integrated SLB for traffic distribution
- **Monitoring**: Arms Prometheus for metrics
- **Logging**: Logtail for centralized logging
- **Ingress**: Nginx ingress controller

## Cleanup

```bash
terraform destroy
```

## Notes

- The cluster is created with managed mode, reducing operational overhead
- Terway CNI plugin is used for networking
- All resources are tagged for cost allocation and management
- Security groups are configured for HTTP/HTTPS access

