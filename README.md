# Cloud-Based IoT Environmental Telemetry Platform (CS361)

Repo: `cs361-iot-cloud-telemetry-platform`  
Team: Seid Cubro (Project Lead — Cloud / Infrastructure / Security) + Charles Shoppel (App / UI)  
Current phase: EKS deployment with API-key-protected ingestion, SQS buffering, DynamoDB persistence, worker-based alert generation, and API endpoints for latest telemetry and alerts.

## What this project is
This repository contains a cloud-native IoT telemetry platform for collecting environmental readings from an ESP32 + DHT sensor and serving them to downstream clients.

### Current production-style data flow
`Device / publisher -> Ingestion service -> SQS -> Worker -> DynamoDB -> API -> UI`

### Current deployed behavior
- `ingestion` accepts telemetry over HTTP and requires an `x-api-key` header.
- `worker` consumes queued telemetry from SQS and writes readings to DynamoDB.
- `worker` also creates alert records when thresholds are exceeded.
- `api` returns latest telemetry and recent alerts for the UI.

## Current architecture snapshot
### Core AWS services
- Amazon EKS for container orchestration
- Amazon SQS for asynchronous buffering
- Amazon DynamoDB for telemetry and alert storage
- Amazon ECR for container images
- Kubernetes Secrets for runtime configuration in the current course-project deployment

### DynamoDB tables
#### `Telemetry`
- Partition key: `device_id` (String)
- Sort key: `timestamp` (Number)

#### `Alerts`
- Partition key: `device_id` (String)
- Sort key: `timestamp` (Number)

## Current API surface
### Ingestion service
- `GET /health`
- `POST /v1/telemetry`

### API service
- `GET /health`
- `GET /v1/telemetry/latest?device_id=<device_id>`
- `GET /v1/alerts`
- `GET /v1/alerts?device_id=<device_id>`

## Telemetry payload format
```json
{
  "house_id": "house-1",
  "device_id": "garage",
  "temperature_f": 70.0,
  "humidity_pct": 40.0,
  "timestamp": 1741800000
}
```

Notes:
- `timestamp` is Unix epoch time in seconds.
- If `timestamp` is omitted, ingestion fills it in automatically.
- `temperature_f` and `humidity_pct` are stored in DynamoDB as numeric values.

## Alert rules
The worker currently creates alert records when:
- `temperature_f > 90`
- `humidity_pct > 80`

Alert records are stored in the `Alerts` table and exposed through the API for UI consumption.

## Repository map
| Path | Purpose |
|---|---|
| `services/` | Application services: ingestion, worker, and api |
| `k8s-eks/` | Current EKS deployment manifests |
| `k8s/` | Historical local kind manifests kept for milestone evidence |
| `docs/` | Project documentation, operations notes, and milestone evidence |
| `project-proposal/` | Proposal deliverables |
| `project-architecture/` | Architecture package and diagrams |
| `project-cdr/` | Critical design review deliverables |
| `project-team-roles/` | Team role assignment document |
| `ESP32_DHT_Sensor_Project_Public_Copy/` | Microcontroller-side publisher sketch |
| `docker-compose.yml` | Historical M4 prototype stack, retained for coursework traceability |

## Quick navigation
- Start here for project docs: `docs/README.md`
- API contract: `docs/api/openapi.yaml`
- Operations runbook: `docs/runbook.md`
- Troubleshooting notes: `docs/troubleshooting.md`
- AWS resource notes: `docs/aws-console-setup.md`
- Milestone evidence map: `docs/milestones.md`

## Historical milestone note
This repository contains both the current EKS-based implementation and older milestone artifacts.

### Historical artifacts retained intentionally
- `docker-compose.yml` and `data/latest.json` support the earlier local-file prototype narrative.
- `k8s/` and `kind-config.yaml` support Milestone M6 local Kubernetes evidence.
- The current implementation path for the backend is the `k8s-eks/` deployment plus the AWS-backed services in `services/`.

## Security note
This is a course project, but the repository should still be treated like a real software system.
- Do not commit credentials, API keys, or tokens.
- Prefer secrets in Kubernetes or environment variables.
- For a future hardening pass, migrate from static AWS credentials to IAM roles for service accounts.

See `SECURITY.md` for the repo policy.
