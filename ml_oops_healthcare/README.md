# ML-OOPS Healthcare Platform

A scalable platform for monitoring and ensuring safety in medical imaging AI models.

## Project Structure

```
ml_oops_healthcare/
├── services/                  # Microservices
│   ├── ml-api/               # Main ML API service
│   │   ├── src/
│   │   │   ├── api/         # API endpoints
│   │   │   ├── storage/     # Database models
│   │   │   └── model.py     # ML model implementation
│   │   └── requirements.txt
│   ├── monitoring-api/       # Monitoring service
│   │   ├── src/
│   │   │   └── monitoring/  # Monitoring implementation
│   │   └── requirements.txt
│   ├── frontend/            # React frontend
│   │   ├── src/
│   │   │   ├── components/  # Reusable components
│   │   │   ├── pages/      # Page components
│   │   │   └── contexts/   # React contexts
│   │   └── package.json
│   └── model-training/      # Model training service
│
├── infrastructure/          # Infrastructure as Code
│   ├── kubernetes/         # K8s configurations
│   ├── terraform/          # Infrastructure provisioning
│   ├── monitoring/         # Monitoring configs
│   │   ├── grafana/       # Grafana dashboards
│   │   └── prometheus.yml # Prometheus config
│   └── docker/            # Docker configurations
│       ├── ml-api.Dockerfile
│       └── docker-compose.yml
│
├── docs/                   # Documentation
│   ├── architecture/      # Architecture docs
│   ├── api/              # API documentation
│   └── deployment/       # Deployment guides
│
├── scripts/              # Utility scripts
│   ├── deployment/      # Deployment scripts
│   └── data-processing/ # Data processing scripts
│
├── tests/               # Test suites
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/           # End-to-end tests
│
└── archive/            # Archived files
```

## Services

1. ML API Service
- Main service for ML model inference
- Handles model versioning and deployment
- Provides REST API for predictions

2. Monitoring API
- Collects model performance metrics
- Handles audit logging
- Provides monitoring endpoints

3. Frontend Service
- React-based dashboard
- Role-based access control
- Real-time monitoring UI

4. Model Training Service (TODO)
- Handles model training pipelines
- Manages training data
- Performs model validation

## Getting Started

### Development Setup

1. Start the development environment:
```bash
cd infrastructure/docker
docker-compose up -d
```

2. Run the frontend:
```bash
cd services/frontend
npm install
npm run dev
```

3. Access the services:
- Frontend: http://localhost:50711
- ML API: http://localhost:57763
- Grafana: http://localhost:3000

### Production Deployment

See [deployment documentation](docs/deployment/README.md) for production setup.

## Additional Repositories Needed

1. **ml-oops-model-registry**
- Purpose: Model versioning and artifact storage
- Key features:
  * Model versioning
  * Artifact storage
  * Model metadata
  * A/B testing support

2. **ml-oops-data-pipeline**
- Purpose: Data processing and training pipelines
- Key features:
  * Data validation
  * Feature engineering
  * Training pipelines
  * Data versioning

3. **ml-oops-compliance**
- Purpose: Compliance and audit management
- Key features:
  * HIPAA compliance checks
  * Audit trail management
  * Policy enforcement
  * Compliance reporting

4. **ml-oops-infrastructure**
- Purpose: Infrastructure as Code
- Key features:
  * Terraform modules
  * Kubernetes configurations
  * CI/CD pipelines
  * Security configurations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.