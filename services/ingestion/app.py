import os
import json
import time

import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

AWS_REGION = env("AWS_REGION")
SQS_QUEUE_URL = env("SQS_QUEUE_URL")

sqs = boto3.client("sqs", region_name=AWS_REGION)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/v1/telemetry")
def ingest():
    data = request.get_json(force=True)

    for k in ["house_id", "device_id", "temperature_f", "humidity_pct"]:
        if k not in data:
            return jsonify({"error": f"Missing field: {k}"}), 400

    if not data.get("timestamp"):
        data["timestamp"] = int(time.time())

    try:
        data["timestamp"] = int(data["timestamp"])
    except (TypeError, ValueError):
        return jsonify({"error": "timestamp must be unix seconds as an integer"}), 400

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(data),
    )

    return jsonify({"message": "Accepted"}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
