#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required for this example" >&2
  exit 1
fi

: "${BASE_URL:?Set BASE_URL env var}"
: "${API_KEY:?Set API_KEY env var}"

resource_key="example-resource-$RANDOM"
subject_id="user-$RANDOM"
echo "Creating resource: $resource_key"
resource=$(curl -sS -X POST "$BASE_URL/v1/resources" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"resource_key\":\"$resource_key\",\"description\":\"example\"}")
echo "Resource created: $resource"

echo "Creating quota rule"
curl -sS -X POST "$BASE_URL/v1/quota-rules" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"resource_key\":\"$resource_key\",\"quota_policy\":\"limited\",\"quota_limit\":100,\"reset_strategy\":{\"unit\":\"day\",\"interval\":1},\"enforcement_mode\":\"enforced\"}" >/dev/null

echo "Checking quota"
check=$(curl -sS -X POST "$BASE_URL/v1/quota/check" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"resource_key\":\"$resource_key\",\"subject_id\":\"$subject_id\",\"amount\":1}")
echo "Check response: $check"

echo "Consuming quota"
consume=$(curl -sS -X POST "$BASE_URL/v1/quota/consume" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"resource_key\":\"$resource_key\",\"subject_id\":\"$subject_id\",\"amount\":1,\"request_id\":\"req-$RANDOM\"}")
echo "Consume response: $consume"
