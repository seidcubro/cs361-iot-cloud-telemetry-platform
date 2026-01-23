from flask import Flask, request, jsonify
import json, os
from datetime import datetime, timezone

app = Flask(__name__)
DATA_PATH = os.environ.get("DATA_PATH", "/data/latest.json")

REQUIRED_FIELDS = ["device_id", "timestamp", "temperature_c", "humidity_pct"]

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f)

@app.get("/health")
def health():
    return jsonify(status="ok", service="ingestion")

@app.post("/v1/telemetry")
def ingest():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify(error="Invalid JSON"), 400

    missing = [k for k in REQUIRED_FIELDS if k not in payload]
    if missing:
        return jsonify(error="Missing fields", missing=missing), 400

    try:
        float(payload["temperature_c"])
        float(payload["humidity_pct"])
    except ValueError:
        return jsonify(error="temperature_c and humidity_pct must be numbers"), 400

    if not payload["timestamp"]:
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()

    data = load_data()
    data[payload["device_id"]] = payload
    save_data(data)

    app.logger.info("Prototype: telemetry accepted (would enqueue to SQS)")
    return jsonify(message="Accepted"), 202
