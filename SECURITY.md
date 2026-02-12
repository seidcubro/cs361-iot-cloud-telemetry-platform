# Security Policy (Course Project)

## Do not commit secrets
Never commit:
- AWS access keys
- API keys
- passwords
- tokens
- `.env` files with credentials

## Recommended local secret handling
- Local Docker: use `.env` (gitignored) or environment variables
- Local kind: use Kubernetes Secrets
- AWS/EKS: use IRSA + Secrets Manager

## IAM least privilege
Grant only the exact permissions required for:
- Ingestion: `sqs:SendMessage`
- Worker: `sqs:ReceiveMessage/DeleteMessage`, `dynamodb:PutItem`
- API: `dynamodb:Query`, optionally `sqs:GetQueueAttributes` for ingestion view

Scope permissions to the specific queue/table resources, not `*`.

## Reporting vulnerabilities
This is an academic project. If you identify a security issue, open a GitHub issue with:
- Impact
- Reproduction steps
- Suggested mitigation
