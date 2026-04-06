# Local Development (Historical Docker Compose Prototype)

This document describes the earlier local prototype kept in the repository for milestone traceability.

## Important status note
The repository's current primary backend path is AWS-backed:
- ingestion -> SQS -> worker -> DynamoDB -> API

The `docker-compose.yml` file is retained to document the M4 prototype, but it is not the mainline environment for the current backend. The current service code has moved beyond the original local-file-only flow.

## What the prototype represented
The original compose stack demonstrated:
- a REST ingestion service
- a REST read service
- shared local storage through `data/latest.json`

That prototype was useful for early milestone evidence before the AWS queue and DynamoDB path replaced it.

## Historical commands
From repo root:
```powershell
docker compose up --build
```

Stop:
```powershell
docker compose down
```

## Historical test pattern
```powershell
curl.exe -i http://localhost:8081/health
curl.exe -i http://localhost:8082/health
```

```powershell
curl.exe -i -X POST "http://localhost:8081/v1/telemetry" `
  -H "Content-Type: application/json" `
  --data-binary "@telemetry.json"
```

## Why this doc still exists
This repo intentionally preserves milestone history. Reviewers can still trace the platform's evolution from:
1. local prototype
2. local Kubernetes proof
3. AWS-backed async pipeline

For the current deployment path, use:
- `docs/aws-console-setup.md`
- `docs/runbook.md`
- `k8s-eks/`
