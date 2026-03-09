import os
import boto3
from flask import Flask, jsonify
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

AWS_REGION = env("AWS_REGION")
DDB_TABLE = env("DDB_TABLE")
SQS_QUEUE_URL = env("SQS_QUEUE_URL")

ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = ddb.Table(DDB_TABLE)

sqs = boto3.client("sqs", region_name=AWS_REGION)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/v1/devices/<device_id>/telemetry/latest")
def latest(device_id: str):
    resp = table.query(
        KeyConditionExpression=Key("device_id").eq(device_id),
        ScanIndexForward=False,
        Limit=1
    )
    items = resp.get("Items", [])
    if not items:
        return jsonify({"error": "No telemetry found"}), 404
    return jsonify(items[0]), 200

# M7 ingestion view: show queue backlog
@app.get("/v1/ingestion/queue")
def queue_view():
    attrs = sqs.get_queue_attributes(
        QueueUrl=SQS_QUEUE_URL,
        AttributeNames=["ApproximateNumberOfMessagesVisible", "ApproximateNumberOfMessagesNotVisible"]
    )["Attributes"]

    return jsonify({
        "queue_depth_visible": int(attrs.get("ApproximateNumberOfMessagesVisible", "0")),
        "queue_inflight_not_visible": int(attrs.get("ApproximateNumberOfMessagesNotVisible", "0"))
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
