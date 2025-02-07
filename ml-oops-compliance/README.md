# ML-OOPS Compliance Service

A comprehensive compliance and audit management system for healthcare AI models, focusing on HIPAA compliance, audit trails, and policy enforcement.

## Features

- HIPAA compliance monitoring
- Automated audit trail generation
- Policy enforcement
- Compliance reporting
- Security scanning
- Access control validation

## Architecture

```
ml-oops-compliance/
├── audit/                  # Audit Service
│   └── src/
│       ├── collectors/    # Audit data collectors
│       ├── analyzers/     # Audit data analysis
│       └── reporters/     # Audit reporting
│
├── policies/              # Policy Service
│   └── src/
│       ├── rules/        # Policy rules
│       ├── validators/   # Policy validation
│       └── enforcers/    # Policy enforcement
│
├── reporting/            # Reporting Service
│   └── src/
│       ├── generators/   # Report generation
│       └── templates/    # Report templates
│
├── validation/           # Validation Service
│   └── src/
│       ├── checks/       # Compliance checks
│       └── scanners/     # Security scanners
│
├── docs/                 # Documentation
│   ├── architecture/    # Architecture docs
│   ├── policies/       # Policy docs
│   └── compliance/     # Compliance docs
│
├── infrastructure/      # Infrastructure configs
│   ├── docker/         # Docker configs
│   └── kubernetes/     # K8s configs
│
└── tests/              # Test suites
    ├── unit/          # Unit tests
    └── integration/   # Integration tests
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Elasticsearch
- Redis

### Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start services:
```bash
docker-compose up -d
```

### Usage Examples

1. Audit Trail Collection:
```python
from audit.src.collectors import ActivityCollector
from audit.src.analyzers import ComplianceAnalyzer

# Collect activity data
collector = ActivityCollector()
activities = collector.collect_activities(
    system_id="ml-model-1",
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-31T23:59:59Z"
)

# Analyze compliance
analyzer = ComplianceAnalyzer()
compliance_report = analyzer.analyze_activities(activities)
```

2. Policy Enforcement:
```python
from policies.src.enforcers import PolicyEnforcer
from policies.src.rules import HIPAARule

# Create policy enforcer
enforcer = PolicyEnforcer()

# Add HIPAA rules
enforcer.add_rule(HIPAARule.DATA_ENCRYPTION)
enforcer.add_rule(HIPAARule.ACCESS_CONTROL)
enforcer.add_rule(HIPAARule.AUDIT_LOGGING)

# Check compliance
compliance_status = enforcer.check_compliance(
    system_id="ml-model-1",
    context={
        "data_encryption": "AES-256",
        "access_control": "RBAC",
        "audit_logging": "enabled"
    }
)
```

3. Compliance Reporting:
```python
from reporting.src.generators import ComplianceReportGenerator
from datetime import datetime, timedelta

# Generate compliance report
generator = ComplianceReportGenerator()
report = generator.generate_report(
    system_id="ml-model-1",
    report_type="hipaa",
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now()
)

# Export report
report.export_pdf("compliance_report.pdf")
```

## API Documentation

### Audit API

```python
# Record audit event
POST /api/v1/audit/events
{
    "system_id": "ml-model-1",
    "event_type": "model_prediction",
    "user_id": "doctor_123",
    "timestamp": "2024-01-23T10:30:00Z",
    "details": {
        "patient_id": "hash_123",
        "model_version": "1.0.0",
        "prediction_id": "pred_456"
    }
}

# Get audit trail
GET /api/v1/audit/trail?system_id=ml-model-1&start_date=2024-01-01&end_date=2024-01-31
```

### Policy API

```python
# Check policy compliance
POST /api/v1/policies/check
{
    "system_id": "ml-model-1",
    "policy_type": "hipaa",
    "context": {
        "data_encryption": "AES-256",
        "access_control": "RBAC",
        "audit_logging": "enabled"
    }
}

# Get policy requirements
GET /api/v1/policies/requirements?policy_type=hipaa
```

### Reporting API

```python
# Generate compliance report
POST /api/v1/reports/generate
{
    "system_id": "ml-model-1",
    "report_type": "hipaa",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "format": "pdf"
}

# Get report status
GET /api/v1/reports/{report_id}/status
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
