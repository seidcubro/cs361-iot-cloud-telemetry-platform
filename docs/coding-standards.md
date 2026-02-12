# Coding Standards (Professional/Industry)

## Python
- Use module docstrings for each service.
- Use function docstrings for non-trivial functions.
- Validate inputs at API boundaries.
- Prefer explicit environment variable configuration (`ENV_VAR` names documented in README).
- Avoid magic constants; use named constants.
- Log meaningful events: accepted telemetry, validation failures, read misses.

## REST API
- Use clear versioned routes: `/v1/...`
- Return appropriate status codes:
  - 200 OK for reads
  - 202 Accepted for async ingestion
  - 400 for validation errors
  - 404 when device/record not found
  - 500 for unexpected errors

## Security
- Never commit secrets to the repo.
- Use least-privilege IAM policies.
- Prefer managed identity (IRSA) on EKS; use K8s Secret only for local kind.

## Documentation
- Keep docs close to the code (`docs/` folder).
- Every milestone must have an evidence pointer (`docs/milestones.md`).
- Keep evidence screenshots/PDFs immutable once submitted.

## Terminal-only workflow
- All file creation/edits should be reproducible via PowerShell commands (heredocs / Set-Content).
- Avoid manual GUI editors during development for this course project.
