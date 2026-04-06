# Documentation Index

This folder contains the documentation and evidence for both the current AWS-backed implementation and earlier course milestones.

## Start here
- `api/openapi.yaml` — current API contract for ingestion and read endpoints
- `aws-console-setup.md` — AWS resource layout and deployment assumptions
- `runbook.md` — operational steps for deployment, rollout checks, and verification
- `troubleshooting.md` — common issues encountered during local and EKS work
- `milestones.md` — evidence map from proposal through the current backend state
- `coding-standards.md` — repo expectations for code and docs changes

## Environment-specific docs
- `local-dev.md` — historical M4 Docker Compose prototype notes
- `kubernetes.md` — historical kind / M6 notes plus current EKS manifest guidance

## Evidence folders
- `pdr-evidence/` — Milestone M4 evidence
- `k8s-deployment-evidence/` — Milestone M6 evidence

## Recommended reading order for reviewers
1. `../README.md`
2. `milestones.md`
3. `api/openapi.yaml`
4. `runbook.md`
5. `aws-console-setup.md`

> The repository intentionally preserves older milestone artifacts. When current behavior and older milestone materials differ, the current source code in `services/` and the current deployment manifests in `k8s-eks/` are the source of truth.
