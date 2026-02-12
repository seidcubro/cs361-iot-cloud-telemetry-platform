"""cs361.services.api

API Service (prototype)

Responsibilities (by milestone):
- M4/M6: Read latest telemetry from a local JSON file shared via a volume.
- M7+: Read telemetry from DynamoDB (time-series per device) as defined in the
  Architecture Package (Partition key=device_id, Sort key=timestamp ISO-8601).

This service intentionally stays small and focused: it exposes REST endpoints for
clients and keeps persistence details behind a simple read function.

Environment variables:
- DATA_PATH: Path to prototype JSON storage (default: /data/latest.json)

Endpoints:
- GET /health
- GET /v1/devices/<device_id>/telemetry/latest
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from flask import Flask, jsonify

app = Flask(__name__)

DATA_PATH = os.environ.get("DATA_PATH", "/data/latest.json")


def load_data() -> Dict[str, Any]:
    """Load prototype telemetry data from DATA_PATH.

    The prototype schema is a dict keyed by device_id:
    {
      "esp32-001": { "device_id": "...", "timestamp": "...", "temperature_c": 22.1, "humidity_pct": 41.2 },
      ...
    }

    Returns:
        dict: Parsed JSON content or an empty dict if the file does not exist or is invalid.
    """
    if not os.path.exists(DATA_PATH):
        return {}

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Treat read/parse failures as "no data" for the prototype.
        return {}


@app.get("/health")
def health():
    """Health endpoint used for readiness/liveness checks."""
    return jsonify(status="ok", service="api"), 200


@app.get("/v1/devices/<device_id>/telemetry/latest")
def latest(device_id: str):
    """Return the latest telemetry record for the given device_id.

    In the prototype implementation, this reads from a shared JSON file.
    In M7+, this will be replaced with a DynamoDB query:
    Query(device_id, ScanIndexForward=False, Limit=1)

    Args:
        device_id: Device identifier (e.g., esp32-001)

    Returns:
        200 + JSON record if found, else 404.
    """
    data = load_data()
    if device_id not in data:
        return jsonify(error="Device not found"), 404
    return jsonify(data[device_id]), 200
