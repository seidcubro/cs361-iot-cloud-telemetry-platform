import os
import json
import time
import traceback
from datetime import datetime, timezone
from decimal import Decimal

import boto3

def env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

AWS_REGION = env("AWS_REGION")
SQS_QUEUE_URL = env("SQS_QUEUE_URL")
DDB_TABLE = env("DDB_TABLE")

sqs = boto3.client("sqs", region_name=AWS_REGION)
ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = ddb.Table(DDB_TABLE)

def safe_json(body: str):
    try:
        return json.loads(body)
    except Exception:
        return None

def to_decimal(x):
    # DynamoDB via boto3 requires Decimal for all numeric types
    return Decimal(str(x))

def normalize(payload: dict) -> dict:
    for k in ["device_id", "temperature_c", "humidity_pct"]:
        if k not in payload:
            raise ValueError(f"Missing field: {k}")

    ts = payload.get("timestamp")
    if not ts:
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    return {
        "device_id": str(payload["device_id"]),
        "timestamp": str(ts),
        "temperature_c": to_decimal(payload["temperature_c"]),
        "humidity_pct": to_decimal(payload["humidity_pct"]),
    }

def main():
    print(f"[worker] start region={AWS_REGION} table={DDB_TABLE}", flush=True)

    while True:
        try:
            resp = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
                VisibilityTimeout=30
            )

            msgs = resp.get("Messages", [])
            if not msgs:
                continue

            for m in msgs:
                receipt = m["ReceiptHandle"]
                body = m.get("Body") or ""
                payload = safe_json(body)

                if payload is None:
                    print(f"[worker] skipping invalid JSON body={body[:120]!r}", flush=True)
                    sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt)
                    continue

                item = normalize(payload)
                table.put_item(Item=item)
                sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt)
                print(f"[worker] processed device_id={item['device_id']} ts={item['timestamp']}", flush=True)

        except Exception as e:
            print("[worker] ERROR:", str(e), flush=True)
            traceback.print_exc()
            time.sleep(2)

if __name__ == "__main__":
    main()
