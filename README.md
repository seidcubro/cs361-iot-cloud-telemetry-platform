# Cloud-Based IoT Environmental Telemetry Platform (CS361)

Repo: `cs361-iot-cloud-telemetry-platform`  
Team: Seid Cubro (Project Lead — Cloud/Infra/Security) + Charles Shoppel (App/DevOps)  
Last updated: 2026-02-12

## 0. What this is
A cloud-native IoT telemetry platform that ingests temperature/humidity readings (ESP32 + DHT22), buffers ingestion asynchronously, persists to DynamoDB, and exposes read APIs.

**Target AWS data flow (final architecture):**

`ESP32 → API Gateway → Ingestion (EKS) → SQS → Worker (EKS) → DynamoDB → API (EKS) → Clients`

This architecture and the design decisions are documented in:
- `project-proposal/CS 361 Project Proposal.pdf`
- `project-architecture/CS 361 Project Architecture Package.pdf`
- `project-team-roles/CS 361 Project Team Roles.pdf`

## 1. Repo map
| Path | Purpose |
|---|---|
| `services/` | Microservices (containerized) |
| `docker-compose.yml` | Local prototype orchestration (Milestone M4) |
| `k8s/` | Kubernetes manifests (Milestone M6) |
| `kind-config.yaml` | Local kind cluster config (Windows) |
| `metrics-server-patch.json` | Patch used to fix metrics-server args for HPA |
| `docs/` | Evidence + milestone documentation (screenshots, PDFs, run notes) |
| `data/latest.json` | **Prototype-only** storage used for M4/M6 local demos (replaced by DynamoDB in M7+) |
| `telemetry.json` | Sample telemetry payload used for testing |

## 2. Current milestone status
- **M4 (PDR):** Local prototype via Docker Compose (ingest + latest read) + evidence in `docs/pdr-evidence/`
- **M5 (CDR):** CDR/traceability/security/observability baseline artifacts in `project-cdr/` (if present)
- **M6:** kind deployment + Services + Ingress + HPA + metrics proof in `docs/k8s-deployment-evidence/`
- **M7 (next):** Replace prototype storage with **SQS + Worker + DynamoDB**, add ingestion view endpoint, and use either a publisher script or the physical ESP32 device.

## 3. Local quickstart (Docker Compose)
**Requirements**
- Docker Desktop
- PowerShell
- Ports available: `8081` (ingestion), `8082` (api)

Run:
```powershell
docker compose up --build
```

Health checks:
```powershell
curl.exe -i http://localhost:8081/health
curl.exe -i http://localhost:8082/health
```

POST telemetry:
```powershell
curl.exe -i -X POST "http://localhost:8081/v1/telemetry" `
  -H "Content-Type: application/json" `
  --data-binary "@telemetry.json"
```

GET latest:
```powershell
curl.exe -i "http://localhost:8082/v1/devices/esp32-001/telemetry/latest"
```

> Note: PowerShell aliases `curl` to `Invoke-WebRequest`. Use `curl.exe` to avoid quoting/behavior differences.

## 4. Kubernetes quickstart (kind)
This repo supports M6 evidence using a local Kubernetes cluster.

Create cluster:
```powershell
kind create cluster --name cs361 --config .\kind-config.yaml
```

Install ingress + metrics-server as needed (see docs):
- `docs/kubernetes.md`
- `docs/troubleshooting.md`

Build and load images:
```powershell
docker build -t cs361-ingestion:local services\ingestion
docker build -t cs361-api:local services\api

kind load docker-image cs361-ingestion:local --name cs361
kind load docker-image cs361-api:local --name cs361
```

Apply manifests:
```powershell
kubectl apply -f .\k8s
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get hpa
kubectl top nodes
```

## 5. Documentation index
Start here: **`docs/README.md`**.

## 6. Evidence / grading artifacts
- M4 evidence: `docs/pdr-evidence/`
- M6 evidence: `docs/k8s-deployment-evidence/`

## 7. Coding + documentation standards
This repo follows:
- Docstrings + comments for non-obvious logic
- Clear configuration via environment variables
- Minimal dependencies
- "Terminal-only" workflow: all editing and operations are reproducible via PowerShell commands

See:
- `CONTRIBUTING.md`
- `docs/coding-standards.md`
- `docs/api/openapi.yaml`

## 8. Security note
Do **not** commit AWS credentials or secrets. Local-only secrets should be stored using:
- `.env` (gitignored) for local runs, or
- Kubernetes Secrets for local clusters

See: `SECURITY.md` and `docs/aws-console-setup.md`.
