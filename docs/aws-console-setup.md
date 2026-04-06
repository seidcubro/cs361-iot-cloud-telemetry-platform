# AWS Resource Setup (Current Backend)

This document describes the AWS resources used by the current backend.

## Region
- `us-east-1`

## 1. SQS queue
### Queue
- Name: `cs361-telemetry-queue`
- Type: Standard queue

### Recommended settings
- Long polling: 10 seconds
- Visibility timeout: 30 seconds
- Retention: default or course-appropriate value

### Why it exists
The ingestion service returns quickly and decouples device traffic from database writes. The worker then drains the queue asynchronously.

## 2. DynamoDB tables
### `Telemetry`
- Partition key: `device_id` (String)
- Sort key: `timestamp` (Number)
- Billing mode: `PAY_PER_REQUEST`

### `Alerts`
- Partition key: `device_id` (String)
- Sort key: `timestamp` (Number)
- Billing mode: `PAY_PER_REQUEST`

### Why the sort key is numeric
The current implementation uses Unix epoch seconds, which supports chronological ordering and latest-record queries.

## 3. ECR repositories
Required repositories:
- `cs361-ingestion`
- `cs361-worker`
- `cs361-api`

## 4. Kubernetes secrets currently used in EKS
### `aws-creds`
Expected keys:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### `telemetry-secrets`
Expected keys:
- `API_KEY`

## 5. Current environment variables by service
### Ingestion
- `AWS_REGION`
- `SQS_QUEUE_URL`
- `API_KEY`

### Worker
- `AWS_REGION`
- `SQS_QUEUE_URL`
- `TABLE_NAME` or default `Telemetry`
- `ALERTS_TABLE` or default `Alerts`

### API
- `AWS_REGION`
- `TABLE_NAME` or default `Telemetry`
- `ALERTS_TABLE` or default `Alerts`

## 6. Security note
For the class deployment, static credentials were injected through Kubernetes Secrets.
For a real production hardening pass, preferred next steps would be:
- IAM roles for service accounts
- tighter least-privilege IAM policies
- secret rotation
- API Gateway or another front-door auth layer for read endpoints if needed
