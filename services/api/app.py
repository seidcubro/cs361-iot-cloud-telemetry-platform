from flask import Flask, jsonify
import json, os

app = Flask(__name__)
DATA_PATH = os.environ.get("DATA_PATH", "/data/latest.json")

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

@app.get("/health")
def health():
    return jsonify(status="ok", service="api")

@app.get("/v1/devices/<device_id>/telemetry/latest")
def latest(device_id):
    data = load_data()
    if device_id not in data:
        return jsonify(error="Device not found"), 404
    return jsonify(data[device_id]), 200
