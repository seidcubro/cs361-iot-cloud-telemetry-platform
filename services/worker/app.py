import os
import json
from decimal import Decimal

import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
TABLE_NAME = os.getenv("TABLE_NAME", "Telemetry")
ALERTS_TABLE = os.getenv("ALERTS_TABLE", "Alerts")

sqs = boto3.client("sqs", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

table = dynamodb.Table(TABLE_NAME)
alerts_table = dynamodb.Table(ALERTS_TABLE)

TEMP_THRESHOLD = 90
HUMIDITY_THRESHOLD = 80

def to_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    return obj

print("Worker started...")

while True:
    resp = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10,
    )

    messages = resp.get("Messages", [])

    for msg in messages:
        body = json.loads(msg["Body"])

        item = {
            "house_id": body["house_id"],
            "device_id": body["device_id"],
            "timestamp": int(body["timestamp"]),
            "temperature_f": to_decimal(body["temperature_f"]),
            "humidity_pct": to_decimal(body["humidity_pct"]),
        }

        # Store telemetry
        table.put_item(Item=item)

        # 🔥 ALERT LOGIC
        alerts = []

        if body["temperature_f"] > TEMP_THRESHOLD:
            alerts.append({
                "type": "HIGH_TEMP",
                "value": body["temperature_f"]
            })

        if body["humidity_pct"] > HUMIDITY_THRESHOLD:
            alerts.append({
                "type": "HIGH_HUMIDITY",
                "value": body["humidity_pct"]
            })

        for alert in alerts:
            alert_item = {
                "device_id": body["device_id"],
                "timestamp": int(body["timestamp"]),
                "house_id": body["house_id"],
                "type": alert["type"],
                "value": to_decimal(alert["value"])
            }

            print(f"[ALERT] {alert_item}")

            alerts_table.put_item(Item=alert_item)

        # Delete message
        sqs.delete_message(
            QueueUrl=SQS_QUEUE_URL,
            ReceiptHandle=msg["ReceiptHandle"],
        )
