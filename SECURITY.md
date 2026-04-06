# Security Policy (Course Project)

## Do not commit secrets
Never commit:
- AWS access keys
- API keys
- passwords
- tokens
- `.env` files with credentials

## Current security posture
The current backend adds API-key authentication to the ingestion endpoint.
That is appropriate for the course milestone, but it is not the final ideal architecture.

## Recommended secret handling
- Local development: environment variables
- Kubernetes / EKS: Kubernetes Secrets
- Future production hardening: IAM roles for service accounts and a managed secret store

## IAM least privilege
Grant only the permissions each service needs.

### Ingestion
- `sqs:SendMessage`

### Worker
- `sqs:ReceiveMessage`
- `sqs:DeleteMessage`
- `dynamodb:PutItem`

### API
- `dynamodb:Query`
- `dynamodb:Scan` for current alert retrieval behavior

Scope permissions to the specific queue and tables instead of `*`.

## Reporting vulnerabilities
This is an academic project. If you find a security issue, open a GitHub issue describing:
- impact
- reproduction steps
- suggested mitigation
