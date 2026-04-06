# Services

This folder contains the three backend services that make up the current platform.

## Current services
### `ingestion/`
Accepts telemetry over HTTP, validates it, enforces API-key authentication, and pushes accepted events to SQS.

### `worker/`
Consumes telemetry events from SQS, writes them to DynamoDB, and creates alerts when threshold rules are exceeded.

### `api/`
Provides read endpoints for latest telemetry and recent alerts so the UI can display current state and notifications.

## Service relationships
`ingestion -> SQS -> worker -> DynamoDB -> api`

## Notes on historical evolution
The repository originally began with a two-service local prototype:
- ingestion
- api

That older prototype used a shared JSON file. The current implementation is AWS-backed and includes the worker.
