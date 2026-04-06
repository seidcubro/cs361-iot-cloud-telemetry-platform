# Worker Service

## Purpose
The worker consumes telemetry messages from SQS and persists them to DynamoDB.

It also generates alert records for UI consumption.

## Responsibilities
- long-poll SQS for telemetry messages
- parse and normalize the message body
- write telemetry records to `Telemetry`
- create alert records in `Alerts`
- delete successfully processed messages from SQS

## Alert thresholds
- `temperature_f > 90` -> `HIGH_TEMP`
- `humidity_pct > 80` -> `HIGH_HUMIDITY`

## Environment variables
- `AWS_REGION`
- `SQS_QUEUE_URL`
- `TABLE_NAME` — defaults to `Telemetry`
- `ALERTS_TABLE` — defaults to `Alerts`

## Local run
```powershell
pip install -r requirements.txt
$env:AWS_REGION = "us-east-1"
$env:SQS_QUEUE_URL = "<queue-url>"
$env:TABLE_NAME = "Telemetry"
$env:ALERTS_TABLE = "Alerts"
python app.py
```

## Operational note
The worker is the most likely bottleneck during load testing because it is the single asynchronous consumer in the current baseline deployment.
