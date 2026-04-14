import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, request
from flask_cors import CORS

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
