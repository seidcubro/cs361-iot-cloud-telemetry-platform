# Kubernetes Deployment Notes

This repository includes two Kubernetes tracks:

## 1. Historical local Kubernetes track
Used for Milestone M6 evidence.

Relevant files:
- `k8s/`
- `kind-config.yaml`
- `metrics-server-patch.json`
- `docs/k8s-deployment-evidence/`

### Historical kind commands
```powershell
kind create cluster --name cs361 --config .\kind-config.yaml
kubectl apply -f .\k8s
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get hpa
```

This path remains in the repo for grading traceability.

## 2. Current EKS deployment track
The backend currently deployed for the project uses the manifests in `k8s-eks/`.

### Current Kubernetes resources
- `namespace.yaml`
- `ingestion.yaml`
- `worker.yaml`
- `api.yaml`

### Current service exposure model
- `ingestion-svc`: external `LoadBalancer`
- `api-svc`: external `LoadBalancer`
- `worker`: internal deployment only

### Current EKS deployment assumptions
- AWS region: `us-east-1`
- namespace: `telemetry`
- images are pulled from Amazon ECR
- AWS credentials are currently injected through Kubernetes Secrets for the class deployment

### Required secrets
- `aws-creds`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- `telemetry-secrets`
  - `API_KEY`

### EKS apply flow
```powershell
kubectl apply -f .\k8s-eks
amespace.yaml
kubectl apply -f .\k8s-eks\ingestion.yaml
kubectl apply -f .\k8s-eks\worker.yaml
kubectl apply -f .\k8s-eks\api.yaml
```

### Verify deployment
```powershell
kubectl get pods -n telemetry
kubectl get svc -n telemetry
kubectl describe deployment ingestion -n telemetry
kubectl describe deployment worker -n telemetry
kubectl describe deployment api -n telemetry
```

### Current operational note
The image tags committed in the manifests may lag behind the exact image tags used in a live debugging session. During active milestone work, images were sometimes updated with `kubectl set image`. The source code in `services/` is the primary source of truth for application behavior.
