# API Service

## Purpose
Provides read endpoints for telemetry data.

Prototype (M4/M6):
- Reads from shared JSON file mounted at `DATA_PATH` (default `/data/latest.json`).

Target (M7+):
- Query DynamoDB table (Partition key `device_id`, Sort key `timestamp`) to return latest record.

## Endpoints
- `GET /health`
- `GET /v1/devices/<device_id>/telemetry/latest`

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
