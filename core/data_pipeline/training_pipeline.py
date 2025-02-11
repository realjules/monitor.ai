from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'ml-oops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'medical_imaging_pipeline',
    default_args=default_args,
    description='End-to-end pipeline for medical imaging model training',
    schedule_interval='@daily',
    catchup=False
)

# Data ingestion task
ingest_data = KubernetesPodOperator(
    task_id='ingest_data',
    name='data-ingestion',
    namespace='ml-oops',
    image='ml-oops-data-pipeline:latest',
    cmds=['python', '-m', 'ingestion.src.main'],
    arguments=['--date', '{{ ds }}'],
    get_logs=True,
    dag=dag,
    resources={
        'request_cpu': '1',
        'request_memory': '2Gi',
        'limit_cpu': '2',
        'limit_memory': '4Gi'
    }
)

# Data validation task
validate_data = KubernetesPodOperator(
    task_id='validate_data',
    name='data-validation',
    namespace='ml-oops',
    image='ml-oops-data-pipeline:latest',
    cmds=['python', '-m', 'validation.src.main'],
    arguments=['--date', '{{ ds }}'],
    get_logs=True,
    dag=dag,
    resources={
        'request_cpu': '1',
        'request_memory': '2Gi',
        'limit_cpu': '2',
        'limit_memory': '4Gi'
    }
)

# Data processing task
process_data = KubernetesPodOperator(
    task_id='process_data',
    name='data-processing',
    namespace='ml-oops',
    image='ml-oops-data-pipeline:latest',
    cmds=['python', '-m', 'processing.src.main'],
    arguments=['--date', '{{ ds }}'],
    get_logs=True,
    dag=dag,
    resources={
        'request_cpu': '2',
        'request_memory': '4Gi',
        'limit_cpu': '4',
        'limit_memory': '8Gi'
    }
)

# Model training task
train_model = KubernetesPodOperator(
    task_id='train_model',
    name='model-training',
    namespace='ml-oops',
    image='ml-oops-data-pipeline:latest',
    cmds=['python', '-m', 'training.src.main'],
    arguments=['--date', '{{ ds }}'],
    get_logs=True,
    dag=dag,
    resources={
        'request_cpu': '4',
        'request_memory': '8Gi',
        'limit_cpu': '8',
        'limit_memory': '16Gi'
    },
    tolerations=[{
        'key': 'gpu',
        'operator': 'Equal',
        'value': 'true',
        'effect': 'NoSchedule'
    }],
    node_selector={
        'cloud.google.com/gke-accelerator': 'nvidia-tesla-t4'
    }
)

# Model validation task
validate_model = KubernetesPodOperator(
    task_id='validate_model',
    name='model-validation',
    namespace='ml-oops',
    image='ml-oops-data-pipeline:latest',
    cmds=['python', '-m', 'validation.src.model_validation'],
    arguments=['--date', '{{ ds }}'],
    get_logs=True,
    dag=dag,
    resources={
        'request_cpu': '2',
        'request_memory': '4Gi',
        'limit_cpu': '4',
        'limit_memory': '8Gi'
    }
)

# Set task dependencies
ingest_data >> validate_data >> process_data >> train_model >> validate_model