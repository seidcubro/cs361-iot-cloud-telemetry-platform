import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, request
from flask_cors import CORS
from time import time

app = Flask(__name__)
CORS(
    app,
    resources={r"/v1/*": {"origins": "*"}},
    allow_headers=["Content-Type", "x-api-key"],
    methods=["GET", "POST", "OPTIONS"],
)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("TABLE_NAME", "Telemetry")
ALERTS_TABLE = os.getenv("ALERTS_TABLE", "Alerts")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
telemetry_table = dynamodb.Table(TABLE_NAME)
alerts_table = dynamodb.Table(ALERTS_TABLE)

def serialize(item):
    if isinstance(item, list):
        return [serialize(i) for i in item]
    if isinstance(item, dict):
        return {k: serialize(v) for k, v in item.items()}
    if isinstance(item, Decimal):
        return float(item)
    return item

@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, x-api-key"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/v1/telemetry/latest", methods=["GET"])
def latest():
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id required"}), 400

    try:
        resp = telemetry_table.query(
            KeyConditionExpression=Key("device_id").eq(device_id),
            ScanIndexForward=False,
            Limit=1,
        )
        items = resp.get("Items", [])
        if not items:
            return jsonify({"error": "No telemetry found"}), 404
        return jsonify(serialize(items[0])), 200
    except Exception as e:
        return jsonify({"error": "Failed to query telemetry", "details": str(e)}), 500

@app.route("/v1/alerts", methods=["GET"])
def get_alerts():
    device_id = request.args.get("device_id")

    try:
        if device_id:
            resp = alerts_table.query(
                KeyConditionExpression=Key("device_id").eq(device_id),
                ScanIndexForward=False,
                Limit=20,
            )
            items = resp.get("Items", [])
        else:
            resp = alerts_table.scan(Limit=20)
            items = resp.get("Items", [])

        return jsonify(serialize(items)), 200
    except Exception as e:
        return jsonify({"error": "Failed to query alerts", "details": str(e)}), 500
    
@app.route("/v1/telemetry/history", methods=["GET"])
def history():
    device_id = request.args.get("device_id")
    hours = request.args.get("hours", type=int)
    start = request.args.get("start", type=int)
    end = request.args.get("end", type=int)
    limit = request.args.get("limit", default=5000, type=int)
    bucket = request.args.get("bucket", type=int)

    if not device_id:
        return jsonify({"error": "device_id required"}), 400

    try:
        now = int(time())

        # Determine time window
        if hours:
            end_ts = now
            start_ts = now - (hours * 3600)
        elif start and end:
            start_ts = start
            end_ts = end
        else:
            return jsonify({"error": "Provide hours OR start/end"}), 400

        resp = telemetry_table.query(
            KeyConditionExpression=(
                Key("device_id").eq(device_id) &
                Key("timestamp").between(start_ts, end_ts)
            ),
            ScanIndexForward=True,
            Limit=limit,
        )

        items = resp.get("Items", [])
        items = serialize(items)

        if not bucket:
            return jsonify(items), 200

        if bucket <= 0:
            return jsonify({"error": "bucket must be > 0"}), 400

        grouped = {}

        for item in items:
            ts = int(item["timestamp"])
            bucket_key = ts // bucket
            bucket_start = bucket_key * bucket

            if bucket_key not in grouped:
                grouped[bucket_key] = {
                    "timestamp": bucket_start,
                    "temps": [],
                    "humidity": []
                }

            grouped[bucket_key]["temps"].append(float(item["temperature_f"]))
            grouped[bucket_key]["humidity"].append(float(item["humidity_pct"]))

        result = []
        for g in grouped.values():
            result.append({
                "timestamp": g["timestamp"],
                "temperature_f": round(sum(g["temps"]) / len(g["temps"]), 2),
                "humidity_pct": round(sum(g["humidity"]) / len(g["humidity"]), 2)
            })

        result.sort(key=lambda x: x["timestamp"])
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": "Failed to query history",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
