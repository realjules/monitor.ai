# Deployment Guide

This guide covers the deployment of ML-OOPS Healthcare in a production environment.

## Prerequisites

- Kubernetes cluster (GKE, EKS, or AKS)
- Helm 3.x
- kubectl configured
- Docker registry access

## Infrastructure Setup

1. Set up infrastructure using Terraform:
```bash
cd infrastructure/terraform
terraform init
terraform apply
```

2. Configure Kubernetes:
```bash
cd ../kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f configmaps.yaml
```

## Service Deployment

### 1. ML API Service

```bash
kubectl apply -f services/ml-api/k8s/
```

Configuration:
- Replicas: 3 (minimum)
- Resources:
  * CPU: 2 cores
  * Memory: 4Gi
- Autoscaling:
  * Min: 3
  * Max: 10
  * CPU target: 70%

### 2. Monitoring API

```bash
kubectl apply -f services/monitoring-api/k8s/
```

Configuration:
- Replicas: 2
- Resources:
  * CPU: 1 core
  * Memory: 2Gi
- Autoscaling:
  * Min: 2
  * Max: 5
  * CPU target: 70%

### 3. Frontend

```bash
kubectl apply -f services/frontend/k8s/
```

Configuration:
- Replicas: 2
- Resources:
  * CPU: 0.5 core
  * Memory: 1Gi
- Autoscaling:
  * Min: 2
  * Max: 5
  * CPU target: 70%

## Monitoring Setup

1. Deploy Prometheus:
```bash
helm install prometheus prometheus-community/prometheus
```

2. Deploy Grafana:
```bash
helm install grafana grafana/grafana
```

3. Configure dashboards:
```bash
kubectl apply -f infrastructure/monitoring/grafana/dashboards/
```

## Security Considerations

1. Network Policies
```bash
kubectl apply -f infrastructure/kubernetes/network-policies/
```

2. RBAC Setup
```bash
kubectl apply -f infrastructure/kubernetes/rbac/
```

3. Secret Management
- Use Kubernetes secrets for sensitive data
- Consider using HashiCorp Vault for advanced secret management

## Scaling Considerations

1. Database
- Set up read replicas
- Configure connection pooling
- Implement sharding for large datasets

2. Caching
- Deploy Redis cluster
- Configure cache invalidation
- Set up CDN for static assets

3. Load Balancing
- Configure ingress controllers
- Set up SSL termination
- Implement rate limiting

## Monitoring and Alerting

1. Set up alerts in Grafana for:
- High error rates
- Latency spikes
- Resource constraints
- Model performance degradation

2. Configure logging:
- Deploy ELK stack
- Set up log rotation
- Configure log aggregation

## Backup and Recovery

1. Database Backups
- Schedule regular backups
- Test recovery procedures
- Set up point-in-time recovery

2. Configuration Backups
- Back up Kubernetes configs
- Store secrets securely
- Document recovery procedures

## Troubleshooting

Common issues and solutions:

1. High Latency
- Check resource utilization
- Verify database performance
- Check network policies

2. Memory Issues
- Adjust resource limits
- Check for memory leaks
- Monitor garbage collection

3. Database Connection Issues
- Check connection pools
- Verify network connectivity
- Check credentials

## Maintenance

1. Regular Tasks
- Update dependencies
- Rotate credentials
- Clean up old data

2. Updates
- Plan maintenance windows
- Use rolling updates
- Test updates in staging

## Health Checks

Monitor service health:
```bash
kubectl get pods -n ml-oops
kubectl top pods -n ml-oops
kubectl logs -f deployment/ml-api
```

## Rollback Procedures

In case of issues:
```bash
kubectl rollout undo deployment/ml-api
kubectl rollout undo deployment/monitoring-api
kubectl rollout undo deployment/frontend
```