# Services

This folder contains the platform microservices.

## Current services
- `ingestion/` — accepts telemetry payloads via REST
- `api/` — reads latest telemetry via REST

## Planned (M7+)
- `worker/` — consumes SQS messages and writes to DynamoDB

Each service directory contains:
- `app.py` (Flask application)
- `requirements.txt`
- `Dockerfile`
- `README.md` describing service usage and configuration
