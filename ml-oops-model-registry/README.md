# ML-OOPS Model Registry

A scalable and compliant model registry for healthcare AI models, focusing on versioning, validation, and compliance tracking.

## Features

- Model versioning and metadata management
- Artifact storage with versioning
- Model validation and testing
- A/B testing support
- Compliance tracking
- API for model deployment and serving

## Architecture

```
ml-oops-model-registry/
├── api/                    # Registry API Service
│   ├── src/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models/        # Data models
│   │   └── utils/         # Utilities
│   └── tests/             # API tests
│
├── storage/               # Model Storage Service
│   ├── src/
│   │   ├── services/     # Storage services
│   │   └── backends/     # Storage backends (S3, etc.)
│   └── tests/            # Storage tests
│
├── versioning/           # Version Control Service
│   ├── src/
│   │   ├── services/    # Versioning services
│   │   └── git/         # Git integration
│   └── tests/           # Versioning tests
│
├── validation/           # Model Validation Service
│   ├── src/
│   │   ├── checks/      # Validation checks
│   │   └── reports/     # Validation reports
│   └── tests/           # Validation tests
│
├── docs/                 # Documentation
│   ├── api/             # API documentation
│   ├── deployment/      # Deployment guides
│   └── architecture/    # Architecture docs
│
├── infrastructure/       # Infrastructure configs
│   ├── docker/          # Docker configs
│   └── kubernetes/      # K8s configs
│
└── scripts/             # Utility scripts
```

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster (for production)
- S3-compatible storage

### Development Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start development services:
```bash
docker-compose up -d
```

4. Run the API:
```bash
uvicorn api.src.main:app --reload
```

### Production Deployment

See [deployment documentation](docs/deployment/README.md) for production setup.

## API Documentation

### Model Management

```python
# Register a new model
POST /api/v1/models
{
    "name": "pneumonia-detector",
    "version": "1.0.0",
    "framework": "pytorch",
    "metadata": {
        "accuracy": 0.95,
        "dataset_version": "2.1.0"
    }
}

# Get model details
GET /api/v1/models/{model_id}

# List model versions
GET /api/v1/models/{model_id}/versions

# Deploy model version
POST /api/v1/models/{model_id}/versions/{version}/deploy
```

### Validation

```python
# Validate model
POST /api/v1/validation/models/{model_id}
{
    "validation_type": "performance",
    "metrics": ["accuracy", "precision", "recall"]
}

# Get validation results
GET /api/v1/validation/results/{validation_id}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
