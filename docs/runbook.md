# Runbook (Operations)

This runbook documents the current AWS-backed backend workflow.

## Services
### Ingestion service
- Purpose: validate telemetry and enqueue it to SQS
- Health: `GET /health`
- Main endpoint: `POST /v1/telemetry`

### Worker service
- Purpose: consume SQS messages, write telemetry to DynamoDB, and create alerts
- Alert thresholds:
  - `temperature_f > 90`
  - `humidity_pct > 80`

### API service
- Purpose: expose read endpoints for the UI
- Endpoints:
  - `GET /health`
  - `GET /v1/telemetry/latest?device_id=<device_id>`
  - `GET /v1/alerts`
  - `GET /v1/alerts?device_id=<device_id>`

## Pre-deployment checklist
- ECR repositories exist for `cs361-ingestion`, `cs361-worker`, and `cs361-api`
- SQS queue exists
- DynamoDB `Telemetry` table exists
- DynamoDB `Alerts` table exists
- Kubernetes secrets exist in namespace `telemetry`

## Build and push images
Examples:
```powershell
docker build -t 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-ingestion:<tag> .\services\ingestion
docker build -t 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-worker:<tag> .\services\worker
docker build -t 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-api:<tag> .\services\api

docker push 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-ingestion:<tag>
docker push 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-worker:<tag>
docker push 094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-api:<tag>
```

## Rollout commands
```powershell
kubectl set image deployment/ingestion ingestion=094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-ingestion:<tag> -n telemetry
kubectl set image deployment/worker worker=094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-worker:<tag> -n telemetry
kubectl set image deployment/api api=094728020196.dkr.ecr.us-east-1.amazonaws.com/cs361-api:<tag> -n telemetry

kubectl rollout status deployment/ingestion -n telemetry
kubectl rollout status deployment/worker -n telemetry
kubectl rollout status deployment/api -n telemetry
```

## Runtime verification
### Pods and services
```powershell
kubectl get pods -n telemetry
kubectl get svc -n telemetry
```

### Logs
```powershell
kubectl logs deployment/ingestion -n telemetry --tail=100
kubectl logs deployment/worker -n telemetry --tail=100
kubectl logs deployment/api -n telemetry --tail=100
```

### Manual ingestion test
```powershell
Invoke-RestMethod -Method POST `
  -Uri "http://<INGESTION_LOAD_BALANCER>/v1/telemetry" `
  -Headers @{ "x-api-key" = "<API_KEY>" } `
  -ContentType "application/json" `
  -Body '{"house_id":"house-1","device_id":"garage","temperature_f":95,"humidity_pct":40,"timestamp":1741800000}'
```

### Manual alerts test
```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://<API_LOAD_BALANCER>/v1/alerts" 
```

### Manual latest telemetry test
```powershell
Invoke-RestMethod -Method GET `
  -Uri "http://<API_LOAD_BALANCER>/v1/telemetry/latest?device_id=garage"
```

## Useful debugging commands
### Current pod names
```powershell
kubectl get pods -n telemetry
```

### Inspect service routing
```powershell
kubectl describe svc ingestion-svc -n telemetry
kubectl describe svc api-svc -n telemetry
kubectl get endpoints ingestion-svc -n telemetry
kubectl get endpoints api-svc -n telemetry
```

### Verify a route from inside a pod
```powershell
kubectl exec -it <API_POD_NAME> -n telemetry -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8080/health').read().decode())"
```

## Rollback
```powershell
kubectl rollout history deployment/api -n telemetry
kubectl rollout undo deployment/api -n telemetry
```

Repeat the same pattern for ingestion or worker when needed.
