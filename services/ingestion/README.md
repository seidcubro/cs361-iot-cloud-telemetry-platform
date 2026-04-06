# Ingestion Service

## Purpose
The ingestion service is the write entry point for telemetry publishers.

It:
- accepts JSON telemetry payloads
- validates required fields
- auto-populates `timestamp` when missing
- requires an `x-api-key` header
- publishes accepted records to SQS

## Endpoints
- `GET /health`
- `POST /v1/telemetry`

## Required payload fields
- `house_id` (string)
- `device_id` (string)
- `temperature_f` (number)
- `humidity_pct` (number)

## Optional payload field
- `timestamp` (integer, Unix epoch seconds)

## Authentication
Requests to `POST /v1/telemetry` must include:
```text
x-api-key: <API_KEY>
```

## Environment variables
- `AWS_REGION`
- `SQS_QUEUE_URL`
- `API_KEY`

## Local run
```powershell
pip install -r requirements.txt
$env:AWS_REGION = "us-east-1"
$env:SQS_QUEUE_URL = "<queue-url>"
$env:API_KEY = "<api-key>"
python app.py
```

## Container
The container runs Gunicorn bound to `0.0.0.0:8080`.
