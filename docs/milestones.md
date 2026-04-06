# Milestones and Evidence Map

This page maps the course project evolution to repository artifacts.

## Planning and design
### Proposal
- `project-proposal/CS 361 Project Proposal.pdf`

### Architecture package
- `project-architecture/CS 361 Project Architecture Package.pdf`
- `project-architecture/361 Project Diagram.png`

### Team roles
- `project-team-roles/CS 361 Project Team Roles.pdf`

## M4 — Local prototype
Goal:
- prove the basic ingestion and read flow locally

Artifacts:
- `docker-compose.yml`
- `services/ingestion/`
- `services/api/`
- `data/latest.json`
- `telemetry.json`
- `docs/pdr-evidence/`

## M5 — Critical design review
Artifacts:
- `project-cdr/CS 361 Project Critical Design Review.pdf`
- `project-cdr/M4-Presentation-CS361.pdf`

## M6 — Local Kubernetes proof
Goal:
- deploy the prototype to local Kubernetes
- show ingress, autoscaling, and metrics evidence

Artifacts:
- `k8s/`
- `kind-config.yaml`
- `metrics-server-patch.json`
- `docs/k8s-deployment-evidence/`

## M7 — AWS-backed async backend
Goal:
- replace direct/local persistence with asynchronous cloud processing
- introduce worker-based processing and DynamoDB persistence

Artifacts:
- `services/worker/`
- `k8s-eks/`
- `docs/aws-console-setup.md`

Implemented behavior:
- ingestion publishes to SQS
- worker writes to DynamoDB `Telemetry`
- API returns latest telemetry by `device_id`

## M8 — Security, alerts, and UI-ready backend
Goal:
- secure ingestion
- add alert generation
- expose alerts for UI consumption

Implemented behavior:
- API-key-protected ingestion via `x-api-key`
- `Alerts` DynamoDB table
- worker-created `HIGH_TEMP` and `HIGH_HUMIDITY` alerts
- API endpoint `GET /v1/alerts`
- external API load balancer for UI consumption

Primary source files:
- `services/ingestion/app.py`
- `services/worker/app.py`
- `services/api/app.py`
- `k8s-eks/ingestion.yaml`
- `k8s-eks/worker.yaml`
- `k8s-eks/api.yaml`

## Next milestone work
Expected remaining work after backend completion:
- load testing
- bottleneck analysis
- worker scaling / tuning
- UI implementation and demonstration
