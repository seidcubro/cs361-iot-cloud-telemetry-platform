# Milestones and Evidence Map (M1–M10)

This page maps course deliverables to repo artifacts.

## M1–M3 (planning + architecture)
- Proposal: `project-proposal/CS 361 Project Proposal.pdf`
- Architecture package: `project-architecture/CS 361 Project Architecture Package.pdf`
- Team roles: `project-team-roles/CS 361 Project Team Roles.pdf`

## M4 (PDR prototype)
Deliverable: running locally (compose) + endpoint proof
- Evidence: `docs/pdr-evidence/`
- Compose: `docker-compose.yml`
- Services: `services/ingestion`, `services/api`
- Sample payload: `telemetry.json`

## M5 (CDR)
Deliverable: traceability + security/observability baseline
- (If present) `project-cdr/` contains the CDR PDF and traceability artifacts.

## M6 (Kubernetes)
Deliverable: Kubernetes deployment + ingress + autoscaling evidence
- Manifests: `k8s/`
- kind config: `kind-config.yaml`
- metrics patch: `metrics-server-patch.json`
- Evidence: `docs/k8s-deployment-evidence/`

## M7 (Async + worker + ingestion view)
Deliverable: queue/stream + worker + publisher + ingestion view
Planned/Work in progress:
- Add `services/worker`
- Add AWS integration: SQS + DynamoDB
- Add an ingestion view endpoint (queue depth / processed counts)
- Publisher: either PowerShell script or physical ESP32

## M8–M10 (load, cost, readiness, demo, final)
- M8: load testing + tuning + cost controls + operational readiness checklist
- M9: demo
- M10: final release tag + final report PDFs + updated docs
