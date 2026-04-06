import os
from decimal import Decimal

import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("TABLE_NAME", "Telemetry")
ALERTS_TABLE = os.getenv("ALERTS_TABLE", "Alerts")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

telemetry_table = dynamodb.Table(TABLE_NAME)
alerts_table = dynamodb.Table(ALERTS_TABLE)

def serialize(item):
    """Convert Decimal → float for JSON"""
    if isinstance(item, list):
        return [serialize(i) for i in item]
    if isinstance(item, dict):
        return {k: serialize(v) for k, v in item.items()}
    if isinstance(item, Decimal):
        return float(item)
    return item

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/v1/telemetry/latest")
def latest():
    device_id = request.args.get("device_id")

    if not device_id:
        return jsonify({"error": "device_id required"}), 400

    resp = telemetry_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("device_id").eq(device_id),
        ScanIndexForward=False,
        Limit=1,
    )

    items = resp.get("Items", [])
    return jsonify(serialize(items)), 200

# NEW ENDPOINT
@app.get("/v1/alerts")
def get_alerts():
    device_id = request.args.get("device_id")

    if device_id:
        resp = alerts_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("device_id").eq(device_id),
            ScanIndexForward=False,
            Limit=20,
        )
        items = resp.get("Items", [])
    else:
        # fallback: scan (fine for class project)
        resp = alerts_table.scan(Limit=20)
        items = resp.get("Items", [])

    return jsonify(serialize(items)), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
