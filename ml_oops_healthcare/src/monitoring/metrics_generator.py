import time
import random
from datetime import datetime, timedelta
import psycopg2
import json

def connect_db():
    return psycopg2.connect(
        dbname="ml_oops",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

def generate_sample_data():
    conn = connect_db()
    cur = conn.cursor()

    # Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS model_predictions (
        id SERIAL PRIMARY KEY,
        model_id VARCHAR(50),
        patient_id VARCHAR(50),
        prediction FLOAT,
        uncertainty FLOAT,
        timestamp TIMESTAMP,
        metadata JSONB,
        ground_truth FLOAT
    );
    
    CREATE TABLE IF NOT EXISTS audit_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        user_id VARCHAR(50),
        action VARCHAR(100),
        resource_type VARCHAR(50),
        resource_id VARCHAR(50),
        details JSONB
    );
    
    CREATE TABLE IF NOT EXISTS performance_metrics (
        id SERIAL PRIMARY KEY,
        model_id VARCHAR(50),
        metric_name VARCHAR(50),
        metric_value FLOAT,
        timestamp TIMESTAMP,
        window_size VARCHAR(20),
        details JSONB
    );
    """)

    # Generate sample predictions
    models = ["pneumonia_detector_v1", "pneumonia_detector_v2"]
    start_time = datetime.now() - timedelta(days=30)
    
    for i in range(1000):
        model_id = random.choice(models)
        timestamp = start_time + timedelta(minutes=random.randint(0, 43200))
        prediction = random.random()
        uncertainty = random.uniform(0.1, 0.3)
        ground_truth = round(random.random())
        
        cur.execute("""
        INSERT INTO model_predictions 
        (model_id, patient_id, prediction, uncertainty, timestamp, metadata, ground_truth)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            model_id,
            f"PAT_{random.randint(1000, 9999)}",
            prediction,
            uncertainty,
            timestamp,
            json.dumps({
                "device_id": f"DEVICE_{random.randint(1, 5)}",
                "image_quality": random.uniform(0.7, 1.0)
            }),
            ground_truth
        ))

    # Generate audit logs
    actions = ["VIEW", "ANALYZE", "EXPORT", "MODIFY"]
    users = [
        ("RAD_", 5),  # 5 radiologists
        ("COMP_", 3), # 3 compliance officers
        ("ADMIN_", 2) # 2 administrators
    ]

    for i in range(500):
        user_type, count = random.choice(users)
        user_id = f"{user_type}{random.randint(1, count)}"
        timestamp = start_time + timedelta(minutes=random.randint(0, 43200))
        
        cur.execute("""
        INSERT INTO audit_logs
        (timestamp, user_id, action, resource_type, resource_id, details)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            timestamp,
            user_id,
            random.choice(actions),
            "PREDICTION",
            f"PRED_{random.randint(1000, 9999)}",
            json.dumps({
                "ip_address": f"192.168.1.{random.randint(1, 255)}",
                "session_id": f"SESSION_{random.randint(1000, 9999)}"
            })
        ))

    # Generate performance metrics
    metrics = ["accuracy", "precision", "recall", "f1_score", "auc_roc"]
    windows = ["1h", "24h", "7d"]

    for i in range(300):
        timestamp = start_time + timedelta(minutes=random.randint(0, 43200))
        
        cur.execute("""
        INSERT INTO performance_metrics
        (model_id, metric_name, metric_value, timestamp, window_size, details)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            random.choice(models),
            random.choice(metrics),
            random.uniform(0.75, 0.95),
            timestamp,
            random.choice(windows),
            json.dumps({
                "sample_size": random.randint(100, 1000),
                "confidence_interval": random.uniform(0.02, 0.05)
            })
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    generate_sample_data()