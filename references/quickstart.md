# Quickstart

## 1. Create a resource
```http
POST /v1/resources
Content-Type: application/json

{ "name": "example-action" }
```

## 2. Attach a quota rule
```http
POST /v1/quota-rules
Content-Type: application/json

{
  "resource_id": "...",
  "quota_policy": "limited",
  "quota_limit": 100,
  "reset_strategy": "fixed_window",
  "reset_window_seconds": 86400,
  "enforcement_mode": "enforced"
}
```

## 3. Check quota before performing the action
```http
POST /v1/quota/check
Content-Type: application/json

{ "resource_id": "...", "amount": 1 }
```

## 4. Consume quota with an idempotent request ID
```http
POST /v1/quota/consume
Content-Type: application/json

{
  "resource_id": "...",
  "amount": 1,
  "request_id": "unique-operation-id"
}
```

This sequence provides predictable enforcement with retry safety and clear reset times.
