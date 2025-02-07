# ML-OOPS Data Pipeline

A scalable data processing and training pipeline for healthcare AI models, focusing on data quality, validation, and reproducible training.

## Features

- Data ingestion from multiple sources (DICOM, PACS, etc.)
- Data validation and quality checks
- Feature engineering pipelines
- Automated training workflows
- Data versioning and lineage tracking
- Quality metrics and reporting

## Architecture

```
ml-oops-data-pipeline/
├── ingestion/              # Data Ingestion Service
│   └── src/
│       ├── connectors/    # Source connectors
│       └── validators/    # Input validation
│
├── processing/            # Data Processing Service
│   └── src/
│       ├── transforms/   # Data transformations
│       └── features/     # Feature engineering
│
├── validation/           # Data Validation Service
│   └── src/
│       ├── quality/     # Quality checks
│       └── schema/      # Schema validation
│
├── training/            # Model Training Service
│   └── src/
│       ├── pipelines/  # Training pipelines
│       └── metrics/    # Training metrics
│
├── docs/               # Documentation
│   ├── architecture/  # Architecture docs
│   └── pipelines/    # Pipeline docs
│
├── infrastructure/    # Infrastructure configs
│   ├── airflow/      # Airflow DAGs
│   └── kubernetes/   # K8s configs
│
└── tests/            # Test suites
    ├── unit/        # Unit tests
    └── integration/ # Integration tests
```

## Getting Started

### Prerequisites

- Python 3.9+
- Apache Airflow
- Kubernetes cluster
- MinIO/S3 storage

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

3. Start Airflow:
```bash
docker-compose up -d
```

### Pipeline Examples

1. Data Ingestion:
```python
from ingestion.src.connectors.dicom import DicomConnector

# Configure DICOM connector
connector = DicomConnector(
    host="pacs.hospital.com",
    port=11112,
    ae_title="ML-OOPS"
)

# Fetch studies
studies = connector.fetch_studies(
    modality="CT",
    date_range=("2024-01-01", "2024-01-31")
)
```

2. Data Processing:
```python
from processing.src.transforms import ImagePreprocessor
from processing.src.features import FeatureExtractor

# Preprocess images
preprocessor = ImagePreprocessor(
    target_size=(512, 512),
    normalize=True
)

# Extract features
extractor = FeatureExtractor(
    model="densenet121",
    pretrained=True
)
```

3. Training Pipeline:
```python
from training.src.pipelines import ModelTrainer

# Configure trainer
trainer = ModelTrainer(
    model_type="classification",
    architecture="densenet121",
    hyperparameters={
        "learning_rate": 0.001,
        "batch_size": 32
    }
)

# Train model
model = trainer.train(
    train_data=train_dataset,
    val_data=val_dataset,
    epochs=100
)
```

## Airflow DAGs

Example DAG for model training:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-oops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'model_training_pipeline',
    default_args=default_args,
    schedule_interval='@daily'
)

# Define tasks
ingest_data = PythonOperator(
    task_id='ingest_data',
    python_callable=ingest_data_fn,
    dag=dag
)

process_data = PythonOperator(
    task_id='process_data',
    python_callable=process_data_fn,
    dag=dag
)

train_model = PythonOperator(
    task_id='train_model',
    python_callable=train_model_fn,
    dag=dag
)

# Set dependencies
ingest_data >> process_data >> train_model
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
