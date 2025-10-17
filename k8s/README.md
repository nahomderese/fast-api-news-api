# Kubernetes Deployment Manifests

This directory contains Kubernetes manifests for deploying the SWEN AI-Enriched News Pipeline.

## Files

- **deployment.yaml**: Main application deployment, service, and HPA
- **ingress.yaml**: Ingress configuration for external access
- **configmap.yaml**: Configuration data
- **secret.yaml.example**: Example secret configuration (DO NOT use in production)

## Quick Start

### 1. Apply ConfigMap

```bash
kubectl apply -f configmap.yaml
```

### 2. Create Secrets

```bash
# Create secrets securely (don't use the example file in production)
kubectl create secret generic swen-secrets \
  --from-literal=qwen-api-key=YOUR_QWEN_API_KEY \
  --from-literal=image-search-api-key=YOUR_IMAGE_API_KEY \
  --from-literal=video-search-api-key=YOUR_VIDEO_API_KEY
```

### 3. Deploy Application

```bash
kubectl apply -f deployment.yaml
```

### 4. Configure Ingress (Optional)

```bash
# Update ingress.yaml with your domain first
kubectl apply -f ingress.yaml
```

## Verify Deployment

```bash
# Check pods
kubectl get pods -l app=swen-ai-pipeline

# Check service
kubectl get svc swen-ai-pipeline

# Check logs
kubectl logs -l app=swen-ai-pipeline --tail=100 -f

# Check HPA
kubectl get hpa
```

## Access the Application

### Via LoadBalancer

```bash
# Get external IP
kubectl get svc swen-ai-pipeline

# Access the API
curl http://<EXTERNAL-IP>/api/v1/health
```

### Via Port Forward (Development)

```bash
kubectl port-forward svc/swen-ai-pipeline 8000:80

# Access locally
curl http://localhost:8000/api/v1/health
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment swen-ai-pipeline --replicas=5
```

### Auto Scaling

The HPA is configured to automatically scale between 2-10 replicas based on:
- CPU utilization (70%)
- Memory utilization (80%)

## Update Deployment

```bash
# Update image
kubectl set image deployment/swen-ai-pipeline api=swen-ai-pipeline:v2

# Or apply updated manifests
kubectl apply -f deployment.yaml
```

## Monitoring

```bash
# Watch pods
kubectl get pods -w

# Describe deployment
kubectl describe deployment swen-ai-pipeline

# View events
kubectl get events --sort-by='.lastTimestamp'
```

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Service not accessible

```bash
kubectl get endpoints swen-ai-pipeline
kubectl describe svc swen-ai-pipeline
```

### Check resource usage

```bash
kubectl top pods
kubectl top nodes
```

## Cleanup

```bash
kubectl delete -f deployment.yaml
kubectl delete -f ingress.yaml
kubectl delete -f configmap.yaml
kubectl delete secret swen-secrets
```

