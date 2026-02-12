# Kubernetes Deployment (kind)

This project uses **kind** for local Kubernetes (Milestone M6). The same manifests are intended to evolve toward **EKS** for later milestones.

## Prerequisites
- Docker Desktop
- `kubectl`
- `kind`

## Create a cluster
```powershell
kind create cluster --name cs361 --config .\kind-config.yaml
kubectl cluster-info
```

## Build + load images into kind
```powershell
docker build -t cs361-ingestion:local services\ingestion
docker build -t cs361-api:local services\api

kind load docker-image cs361-ingestion:local --name cs361
kind load docker-image cs361-api:local --name cs361
```

## Deploy manifests
```powershell
kubectl apply -f .\k8s
kubectl get pods
kubectl get svc
```

## Ingress (local)
The repo includes an `Ingress` object (`k8s/ingress.yaml`) for milestone requirements.
Depending on your local ingress installation, you may need port-forwarding to test HTTP from the host.

## Autoscaling (HPA) + metrics-server
HPA requires the Kubernetes Metrics API. If `kubectl top nodes` fails, install/patch metrics-server.
This repo includes `metrics-server-patch.json` used to correct args and avoid YAML editing issues.

Verify:
```powershell
kubectl get hpa
kubectl top nodes
```

## Evidence commands (M6)
The M6 evidence screenshot/PDF shows:
- `kubectl get pods`
- `kubectl get svc`
- `kubectl get ingress`
- `kubectl get hpa`
- `kubectl top nodes`

See: `docs/k8s-deployment-evidence/`
