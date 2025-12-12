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
    resource_name = f"example-resource-{uuid.uuid4().hex[:8]}"

    # 1) Create resource
    resource = request("/v1/resources", {"name": resource_name, "description": "example"})
    print("Resource created:", json.dumps(resource, indent=2))

    # 2) Create quota rule
    request(
        "/v1/quota-rules",
        {
            "resource_id": resource["id"],
            "quota_policy": "limited",
            "quota_limit": 100,
            "reset_strategy": "fixed_window",
            "reset_interval_seconds": 86400,
            "enforcement_mode": "enforced",
        },
    )
    print("Quota rule created")

    # 3) Check quota
    check = request("/v1/quota/check", {"resource_id": resource["id"], "amount": 1})
    print("Check response:", json.dumps(check, indent=2))

    # 4) Consume quota
    consume = request(
        "/v1/quota/consume",
        {"resource_id": resource["id"], "amount": 1, "request_id": str(uuid.uuid4())},
    )
    print("Consume response:", json.dumps(consume, indent=2))


if __name__ == "__main__":
    main()
