"""cs361.services.ingestion

Ingestion Service (prototype)

Responsibilities (by milestone):
- M4/M6: Validate telemetry payload and store latest record per device in a local JSON file.
- M7+: Validate telemetry payload and publish an event to SQS (async ingestion), returning 202 quickly.

Environment variables:
- DATA_PATH: Path to prototype JSON storage (default: /data/latest.json)

Endpoints:
- GET /health
- POST /v1/telemetry (returns 202 Accepted on success)
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_PATH = os.environ.get("DATA_PATH", "/data/latest.json")

REQUIRED_FIELDS: List[str] = ["device_id", "timestamp", "temperature_c", "humidity_pct"]


def load_data() -> Dict[str, Any]:
    """Load prototype storage from DATA_PATH.

    Returns:
        dict: Parsed JSON dict, or empty dict if file missing/invalid.
    """
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data: Dict[str, Any]) -> None:
    """Persist prototype storage to DATA_PATH.

    Args:
        data: dict keyed by device_id.
    """
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)


def ensure_timestamp(payload: Dict[str, Any]) -> None:
    """Ensure payload has a timestamp.

    For the prototype, if timestamp is empty, set to current UTC ISO-8601.
    """
    if not payload.get("timestamp"):
        payload["timestamp"] = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )


@app.get("/health")
def health():
    """Health endpoint used for readiness/liveness checks."""
    return jsonify(status="ok", service="ingestion"), 200


@app.post("/v1/telemetry")
def ingest():
    """Accept telemetry payloads.

    Validates schema and numeric fields. On success returns 202 Accepted.

    Prototype behavior:
    - Store the *latest* record per device_id in DATA_PATH.
    - Log an informational message indicating that in M7+ this would publish to SQS.

    Returns:
        202 on accepted payload
        400 on validation errors
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(error="Invalid JSON"), 400

    missing = [k for k in REQUIRED_FIELDS if k not in payload]
    if missing:
        return jsonify(error="Missing fields", missing=missing), 400

    try:
        payload["temperature_c"] = float(payload["temperature_c"])
        payload["humidity_pct"] = float(payload["humidity_pct"])
    except (TypeError, ValueError):
        return jsonify(error="temperature_c and humidity_pct must be numbers"), 400

    ensure_timestamp(payload)

    data = load_data()
    data[str(payload["device_id"])] = payload
    save_data(data)

    app.logger.info("Prototype: telemetry accepted (M7+ will enqueue to SQS)")
    return jsonify(message="Accepted"), 202
