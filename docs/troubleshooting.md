# Troubleshooting

## PowerShell `curl` alias problem
PowerShell aliases `curl` to `Invoke-WebRequest`, which behaves differently from standard curl.

Use one of these instead:
- `curl.exe`
- `Invoke-RestMethod`
- `Invoke-WebRequest`

## Multi-line PowerShell command issue
Linux-style `\` line continuations do not work in PowerShell.
Use either:
- a single line command, or
- PowerShell backticks `` ` ``

## `ImagePullBackOff` on EKS
Common causes:
- not logged into ECR
- pushed the wrong image tag
- deployment points to a tag that does not exist

Typical fix:
```powershell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker push <full-image-tag>
kubectl rollout restart deployment/<name> -n telemetry
```

## Route exists in source but returns 404
Possible causes:
- request is hitting the wrong service or load balancer
- the deployment is still serving an older image tag
- the service is not exposed externally

What worked in this project:
- verify routes inside the pod with `print(app.url_map)`
- verify the route over HTTP from inside the pod
- move to a brand-new immutable image tag instead of reusing an older tag
- confirm the service type and external load balancer

## Service confusion between ingestion and API
This project uses two different public load balancers in the current EKS layout:
- ingestion load balancer for `POST /v1/telemetry`
- API load balancer for read endpoints like `/v1/alerts`

If `/v1/telemetry` works but `/v1/alerts` returns 404, double-check which load balancer URL you are calling.

## `kubectl get pods` returns nothing
By default, `kubectl` uses the `default` namespace.
If the project resources are in `telemetry`, use:
```powershell
kubectl get pods -n telemetry
```

## `kubectl exec` pod not found
Pods are replaced during rollouts, so names change frequently.
Always refresh the pod name first:
```powershell
kubectl get pods -n telemetry
```

## `netstat` not found inside slim images
Minimal Python images often do not include debugging tools like `netstat`.
Use Python-based HTTP checks or `print(app.url_map)` from inside the pod instead.

## Legacy docs versus current implementation
This repository intentionally keeps older milestone artifacts.
If you see conflicting information:
1. trust the source code in `services/`
2. trust the current manifests in `k8s-eks/`
3. treat `docker-compose.yml`, `k8s/`, and earlier evidence folders as historical context

## Browser CORS errors from the UI
If the frontend shows `Access-Control-Allow-Origin` missing:
1. confirm the UI is calling the API load balancer, not the ingestion load balancer
2. make sure `flask-cors` is installed in `services/api/requirements.txt`
3. make sure `CORS(app, ...)` is enabled in `services/api/app.py`
4. rebuild and deploy a fresh API image tag

## Wrong load balancer URL
The ingestion load balancer only supports:
- GET /health
- POST /v1/telemetry

UI read requests must go to the API load balancer:
- GET /v1/telemetry/latest
- GET /v1/alerts