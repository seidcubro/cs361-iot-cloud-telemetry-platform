import os
import json
import time

import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

def env(name: str, required: bool = True, default: str | None = None) -> str | None:
    v = os.getenv(name, default)
    if required and not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

AWS_REGION = env("AWS_REGION")
SQS_QUEUE_URL = env("SQS_QUEUE_URL")
API_KEY = env("API_KEY")

sqs = boto3.client("sqs", region_name=AWS_REGION)

def unauthorized():
    return jsonify({"error": "Unauthorized"}), 401

@app.before_request
def require_api_key():
    if request.path == "/health":
        return None

    incoming_key = request.headers.get("x-api-key")
    if not incoming_key or incoming_key != API_KEY:
        return unauthorized()

    return None

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/v1/telemetry")
def ingest():
    data = request.get_json(force=True, silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    for k in ["house_id", "device_id", "temperature_f", "humidity_pct"]:
        if k not in data:
            return jsonify({"error": f"Missing field: {k}"}), 400

    if data.get("timestamp") in (None, ""):
        data["timestamp"] = int(time.time())

    try:
        data["timestamp"] = int(data["timestamp"])
    except (TypeError, ValueError):
        return jsonify({"error": "timestamp must be unix seconds as an integer"}), 400

    try:
        sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(data),
        )
    except Exception:
        return jsonify({"error": "Failed to enqueue telemetry"}), 500

    return jsonify({"message": "Accepted"}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
