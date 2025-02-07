FROM python:3.9-slim

WORKDIR /app

COPY requirements-monitoring.txt .
RUN pip install --no-cache-dir -r requirements-monitoring.txt

COPY src/api /app/api
COPY src/storage /app/storage
COPY config /app/config

ENV PYTHONPATH=/app

CMD ["python", "api/main.py"]