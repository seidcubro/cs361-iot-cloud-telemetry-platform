# AWS Console Setup (M7+)

This document describes the **AWS Console** configuration required for Milestone M7+:
- SQS queue for asynchronous buffering
- DynamoDB table for time-series storage
- IAM least-privilege permissions
- Optional: Secrets Manager for configuration

> For CS361: AWS resource creation is done in the console to demonstrate cloud proficiency.

## 1) DynamoDB: Telemetry table
Create a DynamoDB table:

- **Table name:** `Telemetry`
- **Partition key:** `device_id` (String)
- **Sort key:** `timestamp` (String, ISO-8601)

Recommended settings:
- **Capacity mode:** On-demand (PAY_PER_REQUEST)
- **Encryption:** default enabled
- **PITR:** enable if budget allows (helps with rollback/ops readiness)

Why:
- Partitioning by `device_id` isolates device data and scales horizontally.
- Sort key `timestamp` supports: latest query (descending + limit 1) and range queries.

## 2) SQS: Standard queue + DLQ
Create:
- Standard queue: `cs361-telemetry-queue`
- Dead-letter queue (DLQ): `cs361-telemetry-dlq`

Recommended settings:
- **Long polling:** 10 seconds
- **Visibility timeout:** 30 seconds
- **Retention:** default 4 days
- **Redrive policy:** max receives 5 → DLQ

Why:
- Long polling reduces API spam/cost.
- Visibility timeout supports retry semantics.
- DLQ prevents poison messages from retrying forever.

## 3) IAM: least privilege
Create a dedicated IAM user or role (development-only) with permissions scoped to:
- The SQS queue ARN (send/receive/delete/get attributes)
- The DynamoDB table ARN (put/query/get/describe)

**Do not** grant `*` resources.

Local kind note:
- Local Kubernetes cannot use IRSA (EKS feature). For M7 local proof, credentials are provided via Kubernetes Secrets.
- For EKS, migrate to IRSA (no static credentials) as a planned improvement.

## 4) API Gateway + API keys (planned)
For device ingestion security, API Gateway can enforce an API key (or JWT) before routing to ingestion.
This is typically implemented after the async pipeline is proven end-to-end.

## 5) What values you will need later
Capture:
- AWS Region (e.g., `us-east-1`)
- SQS Queue URL
- DynamoDB table name
- Access key + secret (development-only)
