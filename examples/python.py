"""Minimal Python example for Thrysha API.
Requires: Python 3.9+ and requests (`pip install requests`).
Set BASE_URL and API_KEY env vars before running.
"""

import os
import sys
import uuid
import json
import requests

BASE = os.environ.get("BASE_URL")
KEY = os.environ.get("API_KEY")

if not BASE or not KEY:
    print("Set BASE_URL and API_KEY env vars to run the example.")
    sys.exit(1)

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"}


def request(path: str, payload: dict | None = None):
    resp = requests.post(f"{BASE}{path}", headers=HEADERS, json=payload) if payload is not None else requests.get(
        f"{BASE}{path}", headers=HEADERS
    )
    if not resp.ok:
        raise SystemExit(f"{resp.status_code} {resp.text}")
    if resp.text:
        return resp.json()
    return None


def main():
    resource_key = f"example-resource-{uuid.uuid4().hex[:8]}"
    subject_id = f"user-{uuid.uuid4().hex[:8]}"

    # 1) Create resource
    resource = request("/v1/resources", {"resource_key": resource_key, "description": "example"})
    print("Resource created:", json.dumps(resource, indent=2))

    # 2) Create quota rule
    request(
        "/v1/quota-rules",
        {
            "resource_key": resource_key,
            "quota_policy": "limited",
            "quota_limit": 100,
            "reset_strategy": {"unit": "day", "interval": 1},
            "enforcement_mode": "enforced",
        },
    )
    print("Quota rule created")

    # 3) Check quota
    check = request("/v1/quota/check", {"resource_key": resource_key, "subject_id": subject_id, "amount": 1})
    print("Check response:", json.dumps(check, indent=2))

    # 4) Consume quota
    consume = request(
        "/v1/quota/consume",
        {"resource_key": resource_key, "subject_id": subject_id, "amount": 1, "request_id": str(uuid.uuid4())},
    )
    print("Consume response:", json.dumps(consume, indent=2))


if __name__ == "__main__":
    main()
