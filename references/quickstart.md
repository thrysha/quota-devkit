# Quickstart

## 1. Create a resource
```http
POST /v1/resources
Content-Type: application/json

{ "resource_key": "example-action", "description": "optional" } // resource_key: lowercase letters/digits, '-' or '_'
```

## 2. Attach a quota rule
```http
POST /v1/quota-rules
Content-Type: application/json

{
  "resource_key": "...",
  "quota_policy": "limited",
  "quota_limit": 100,
  "reset_strategy": { "unit": "day", "interval": 1 }, // hour|day|week|month|year|never
  "enforcement_mode": "enforced"
}
```

## 3. Check quota before performing the action
```http
POST /v1/quota/check
Content-Type: application/json

{ "resource_key": "...", "subject_id": "user_123", "amount": 1 }
```

## 4. Consume quota with an idempotent request ID
```http
POST /v1/quota/consume
Content-Type: application/json

{
  "resource_key": "...",
  "subject_id": "user_123",
  "amount": 1,
  "request_id": "unique-operation-id"
}
```

This sequence provides predictable enforcement with retry safety; when a limit would be exceeded on enforced rules, the consume call returns 200 with `allowed=false` and the current remaining value.
