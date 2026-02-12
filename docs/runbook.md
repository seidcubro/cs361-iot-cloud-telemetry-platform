# Runbook (Operations)

This runbook documents how to operate the system in both local and Kubernetes environments.

## Service health endpoints
- ingestion: `/health`
- api: `/health`

## Common checks (Kubernetes)
```powershell
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get hpa
kubectl top nodes
```

## Viewing logs
```powershell
kubectl logs deploy/ingestion --tail=200
kubectl logs deploy/api --tail=200
```

## Rollback (Kubernetes)
Kubernetes supports rollback to a previous ReplicaSet revision:
```powershell
kubectl rollout history deployment/api
kubectl rollout undo deployment/api
```

## Failure scenarios (planned for M7+)
- Worker down → SQS queue depth increases
- DynamoDB throttling → worker retries, backlog increases
- Recovery: fix worker / scale worker → backlog drains

These scenarios map directly to the architecture package's failure demo narrative.
