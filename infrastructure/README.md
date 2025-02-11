# ML-OOPS Infrastructure

Infrastructure as Code (IaC) repository for ML-OOPS Healthcare platform, containing Terraform modules, Kubernetes configurations, CI/CD pipelines, and security policies.

## Architecture

```
ml-oops-infrastructure/
├── terraform/                    # Infrastructure as Code
│   ├── modules/                 # Reusable modules
│   │   ├── networking/         # Network infrastructure
│   │   ├── compute/           # Compute resources
│   │   ├── storage/           # Storage resources
│   │   └── monitoring/        # Monitoring stack
│   └── environments/          # Environment configs
│       ├── dev/              # Development
│       ├── staging/         # Staging
│       └── prod/           # Production
│
├── kubernetes/              # Kubernetes configs
│   ├── base/              # Base configurations
│   └── overlays/         # Environment overlays
│       ├── dev/         # Development
│       ├── staging/    # Staging
│       └── prod/      # Production
│
├── ci-cd/               # CI/CD configurations
│   ├── github-actions/ # GitHub Actions workflows
│   └── argocd/        # ArgoCD configurations
│
├── security/          # Security configurations
│   ├── policies/     # Security policies
│   └── scanning/    # Security scanning
│
└── docs/           # Documentation
    ├── architecture/ # Architecture docs
    └── deployment/  # Deployment guides
```

## Features

- Infrastructure as Code with Terraform
- Kubernetes configuration management
- CI/CD pipeline definitions
- Security policies and scanning
- Multi-environment support
- Monitoring and logging infrastructure

## Getting Started

### Prerequisites

- Terraform >= 1.0.0
- kubectl >= 1.20
- AWS CLI (configured)
- GitHub CLI
- ArgoCD CLI

### Infrastructure Deployment

1. Initialize Terraform:
```bash
cd terraform/environments/dev
terraform init
```

2. Plan changes:
```bash
terraform plan -out=tfplan
```

3. Apply changes:
```bash
terraform apply tfplan
```

### Kubernetes Deployment

1. Apply base configurations:
```bash
kubectl apply -k kubernetes/base
```

2. Apply environment overlay:
```bash
kubectl apply -k kubernetes/overlays/dev
```

## Infrastructure Components

### 1. Networking

```hcl
module "vpc" {
  source = "../../modules/networking/vpc"
  
  environment = "dev"
  cidr_block  = "10.0.0.0/16"
  
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]
}
```

### 2. Compute

```hcl
module "eks" {
  source = "../../modules/compute/eks"
  
  cluster_name    = "ml-oops-cluster"
  cluster_version = "1.24"
  
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_size = 2
      max_size     = 4
      min_size     = 1
      
      instance_types = ["t3.large"]
    }
    gpu = {
      desired_size = 1
      max_size     = 2
      min_size     = 0
      
      instance_types = ["g4dn.xlarge"]
    }
  }
}
```

### 3. Storage

```hcl
module "s3" {
  source = "../../modules/storage/s3"
  
  bucket_name = "ml-oops-models"
  versioning  = true
  encryption  = true
}
```

### 4. Monitoring

```hcl
module "monitoring" {
  source = "../../modules/monitoring"
  
  cluster_name     = module.eks.cluster_name
  grafana_version  = "8.2.0"
  prometheus_version = "2.30.3"
}
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: ML-OOPS CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          make test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EKS
        run: |
          make deploy
```

## Security

### Policy Example

```yaml
apiVersion: security.k8s.io/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: true
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
