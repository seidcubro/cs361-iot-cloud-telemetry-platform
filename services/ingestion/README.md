# Ingestion Service

## Purpose
Accepts telemetry payloads from devices/publishers.

Prototype (M4/M6):
- Validates payload then stores latest record per device in a JSON file mounted at `DATA_PATH`.

Target (M7+):
- Validates payload then publishes an event to SQS and returns 202 quickly.

## Endpoint
- `POST /v1/telemetry` → `202 Accepted` on success
- `GET /health`

## Telemetry schema
Required fields:
- `device_id` (string)
- `timestamp` (ISO-8601, UTC recommended)
- `temperature_c` (number)
- `humidity_pct` (number)

## Configuration
Environment variables:
- `DATA_PATH` — path to prototype JSON file

## Local run (outside docker)
```powershell
pip install -r requirements.txt
$env:DATA_PATH = "..\..\data\latest.json"
python app.py
```

## Container
`Dockerfile` runs Gunicorn binding to `0.0.0.0:8080`.
