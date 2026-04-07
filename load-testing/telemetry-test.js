import http from "k6/http";
import { check, sleep } from "k6";

const INGEST_URL = "http://aaf245e54c2544f5e9db568b2c31ee82-1754653506.us-east-1.elb.amazonaws.com/v1/telemetry";
const API_KEY = "VBqHnqlbeRKfqXQapWKm7KFeXwXoZ5W7AIItwit6";

export const options = {
    stages: [
        { duration: '30s', target: 25 },
        { duration: '1m', target: 75 },
        { duration: '1m', target: 150 },
        { duration: '30s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.10'],
        http_req_duration: ['p(95)<3000'],
    },
};

export default function () {
    const now = Math.floor(Date.now() / 1000);

    const payload = JSON.stringify({
        house_id: "house-1",
        device_id: `garage-${__VU}`,
        temperature_f: 70 + Math.random() * 30,
        humidity_pct: 35 + Math.random() * 40,
        timestamp: now,
    });

    const params = {
        headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
        },
    };

    const res = http.post(INGEST_URL, payload, params);

    check(res, {
        "status is 202": (r) => r.status === 202,
    });

    sleep(1);
}
