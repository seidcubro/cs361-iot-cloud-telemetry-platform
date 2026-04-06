# API Service

## Purpose
The API service is the read layer for the UI and other clients.

It currently reads from DynamoDB and exposes:
- latest telemetry by `device_id`
- recent alerts, optionally filtered by `device_id`

## Endpoints
- `GET /health`
- `GET /v1/telemetry/latest?device_id=<device_id>`
- `GET /v1/alerts`
- `GET /v1/alerts?device_id=<device_id>`

## Data sources
- DynamoDB table `Telemetry`
- DynamoDB table `Alerts`

## Environment variables
- `AWS_REGION` — AWS region, default `us-east-1`
- `TABLE_NAME` — telemetry table name, default `Telemetry`
- `ALERTS_TABLE` — alerts table name, default `Alerts`

## Response behavior
### Latest telemetry
The current implementation returns a single-item array containing the newest telemetry record for the requested device.

### Alerts
- with `device_id`: performs a DynamoDB query for that device
- without `device_id`: performs a scan limited to 20 records

## Local run
```powershell
pip install -r requirements.txt
$env:AWS_REGION = "us-east-1"
$env:TABLE_NAME = "Telemetry"
$env:ALERTS_TABLE = "Alerts"
python app.py
```

## Container
The container runs Gunicorn bound to `0.0.0.0:8080`.
