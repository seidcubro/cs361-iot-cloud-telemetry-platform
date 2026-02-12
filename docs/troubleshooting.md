# Troubleshooting

## PowerShell curl alias
PowerShell aliases `curl` to `Invoke-WebRequest` (different flags/quoting).
Use `curl.exe`.

## Metrics API not available (HPA)
Symptoms:
- `kubectl top nodes` fails
- HPA shows `TARGETS <unknown>`

Fix:
- Ensure metrics-server is installed and healthy.
- Avoid `kubectl edit` when possible (tabs/indentation can break YAML).
- Use `kubectl patch --patch-file metrics-server-patch.json` as documented by this repo.

Verify:
```powershell
kubectl top nodes
kubectl get hpa
```

## Ingress unreachable in kind
Some kind ingress setups are not bound directly to host `localhost:80`.
If endpoint tests fail but pods/services are healthy:
- use `kubectl port-forward` to reach services for demo
- capture cluster proof for milestone grading

## Docker build issues
- Ensure Dockerfiles are named `Dockerfile` (not `Dockerfile.txt`)
- Rebuild with `--no-cache` if dependency issues occur:
```powershell
docker build --no-cache -t cs361-api:local services\api
```
