# Local Development (Docker Compose)

## Prerequisites
- Windows + PowerShell
- Docker Desktop (WSL2 backend recommended)
- `curl.exe` available (Windows 10/11 includes it)

## Services
- **ingestion**: receives telemetry and accepts payloads (prototype writes to `data/latest.json`)
- **api**: serves read endpoints (prototype reads from `data/latest.json`)

## Run
From repo root:
```powershell
docker compose up --build
```

Stop:
```powershell
docker compose down
```

## Test: health
```powershell
curl.exe -i http://localhost:8081/health
curl.exe -i http://localhost:8082/health
```

## Test: publish telemetry
The repo includes a sample payload in `telemetry.json`.

```powershell
curl.exe -i -X POST "http://localhost:8081/v1/telemetry" `
  -H "Content-Type: application/json" `
  --data-binary "@telemetry.json"
```

Expected:
- HTTP **202 Accepted**
- body: `{"message":"Accepted"}`

## Test: read latest
```powershell
curl.exe -i "http://localhost:8082/v1/devices/esp32-001/telemetry/latest"
```

Expected:
- HTTP **200 OK**
- JSON payload for that device

## PowerShell gotcha: curl alias
PowerShell aliases `curl` to `Invoke-WebRequest`, which changes quoting/flags behavior.
Use `curl.exe` for consistent cross-platform curl behavior.
