# Quota Devkit

Quota is an API-first platform for quota enforcement. It lets teams launch pricing tiers, protect shared resources, and prevent abuse without building their own counters, windows, or reset logic.

## Overview
- **Core concepts**
  - **Resource** — the feature or action being limited (e.g., `api-requests`, `sms-send`, `feature-action`).
  - **subject_id** — who is consuming the resource (e.g., tenant, user, API key, device).
  - **Quota rule** — limit + reset window attached to a resource. Configure `quota_policy` (`limited` or `unlimited`), `enforcement_mode` (`enforced` or `non_enforced`), and `reset_strategy` (hour/day/week/month/year/never; interval > 0 except never).
  - **Idempotency** — `request_id` ensures retries don’t double-consume usage.
- **QuickStart** — get an API key, set `BASE_URL=https://quota-api.thrysha.io`, create a resource, attach a quota rule, then call Check/Consume before doing work (see flows below).
- **Dev Kit** — this repo bundles the Quota API OpenAPI spec, Postman collection, and runnable examples to exercise the flow end to end.

## Introduction (from the API docs)
Most modern products need guardrails on usage.

Examples:
• A dating app caps swipes or messages per user per day
• A SaaS platform limits how often a host can be powered off per hour
• An AI API caps requests per tenant per day

Implementing these limits correctly is harder than it looks: reset semantics, retries, idempotency, and enforcement behavior quickly become operational burdens.

Quota API sits in the request path and makes a deterministic allow/block decision for each request. You define a stable `resource_key`, attach a quota rule that describes limits and reset behavior, then check or consume usage per `subject_id`.

## Example: implementing a daily limit
Goal: set a per-subject daily limit for an action. Workflow:

1) Create a `resource_key` representing the action.  
2) Attach a limited quota rule with a daily reset.  
3) Check or consume usage per subject.

Requests:
```http
1) POST /v1/resources
   → create "sample-resource"

2) POST /v1/quota-rules
   → quota_policy=limited
   → quota_limit=100
   → reset_strategy={ unit: "day", interval: 1 }
   → enforcement_mode=enforced

3) POST /v1/quota/check
   → preflight a request

4) POST /v1/quota/consume
   → record usage with a request_id for idempotency
```

## Environment & Base URL
- Use `https://quota-api.thrysha.io` for all requests and keep environments consistent to avoid mixing tenant data.

## Authentication
- API keys are required on every endpoint. Keep them server-side, rotate regularly, and scope them per environment. Missing or invalid keys are rejected before any work is done.

Headers:
```http
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

## Resources API
### Create Resource
- **Purpose:** register the feature/action you want to meter. Use stable, unique keys so usage stays aligned over time.
- **Request**
  ```http
  POST /v1/resources

  {
    "resource_key": "apples-discard",
    "description": "Used by service A"
  }
  ```
- **Response**
  ```json
  {
    "id": "res_abcd1234",
    "account_id": "acct_123",
    "resource_key": "apples-discard",
    "description": "Used by service A",
    "created_at": "2025-01-10T12:34:56Z"
  }
  ```
- **Business rules**
  - `resource_key` matches `^[a-z0-9][a-z0-9_-]{1,62}$` and is case-insensitively unique per account.
  - Account limit: up to 100,000 resources.
  - Resources belong to the caller’s account; `account_id` cannot be overridden.
- **Errors:** `ERR_RESOURCE_LIMIT_REACHED`, `ERR_RESOURCE_KEY_TAKEN`, 400 invalid payload, 409 duplicates, 401 unauthorized.

### List Resources
- **Purpose:** audit what is being metered, surface IDs for automation, and reconcile against your catalog.
- **Request**
  ```http
  GET /v1/resources?page=1&page_size=50
  ```
- **Response**
  ```json
  {
    "items": [
      { "id": "res_abcd1234", "account_id": "acct_123", "resource_key": "apples-discard", "description": "optional", "created_at": "..." }
    ],
    "page": 1,
    "page_size": 50,
    "total": 1
  }
  ```
- **Business rules:** `page` defaults to 1 (≥ 1); `page_size` defaults to 50 and is capped at 200.
- **Errors:** `ERR_INVALID_PAGINATION`, 400 invalid pagination, 401 unauthorized.

### Delete Resource
- **Purpose:** retire a resource; removes it from future listings. Ensure no active rules depend on it.
- **Request**
  ```http
  DELETE /v1/resources/{resourceKey}
  ```
- **Response**
  ```json
  { "status": "deleted" }
  ```
- **Business rules:** resource must belong to the authenticated account.
- **Errors:** `ERR_RESOURCE_NOT_FOUND`, 404 when missing, 401 unauthorized.

## Quota Rules API
### Create Quota Rule
- **Purpose:** attach a limit and reset window to a resource.
- **Request**
  ```http
  POST /v1/quota-rules

  {
    "resource_key": "apples-discard",
    "quota_limit": 1000,
    "quota_policy": "limited",              // optional, defaults to "limited"
    "reset_strategy": {
      "unit": "hour",                       // hour | day | week | month | year | never
      "interval": 1                         // > 0; ignored for "never"
    },
    "enforcement_mode": "enforced"          // or "non_enforced"
  }
  ```
- **Response**
  ```json
  {
    "id": "qr_123",
    "resource_key": "apples-discard",
    "quota_policy": "limited",
    "quota_limit": 1000,
    "reset_strategy": { "unit": "hour", "interval": 1 },
    "enforcement_mode": "enforced",
    "created_at": "..."
  }
  ```
- **Business rules**
  - `resource_key` must belong to the authenticated account; only one active rule per resource.
  - `quota_policy=limited` enforces a cap (use `enforced` to block, `non_enforced` to measure first).
  - `quota_policy=unlimited` tracks usage without blocking.
  - `reset_strategy.unit` supports hour/day/week/month/year/never; `interval` > 0 except for never. Windows align to UTC boundaries.
  - Creating a rule where one exists returns `ERR_CREATE_QUOTA_RULE_FAILED`.
- **Errors:** 400 invalid fields, 404 missing resource, 401 unauthorized, `ERR_CREATE_QUOTA_RULE_FAILED`.

### List Quota Rules
- **Purpose:** inspect current limits and reset strategies for a resource.
- **Request**
  ```http
  GET /v1/quota-rules?resource_key=apples-discard&page=1&page_size=50
  ```
- **Response**
  ```json
  {
    "items": [
      {
        "id": "qr_123",
        "resource_key": "apples-discard",
        "quota_limit": 1000,
        "quota_policy": "limited",
        "reset_strategy": { "unit": "hour", "interval": 1 },
        "enforcement_mode": "enforced",
        "created_at": "..."
      }
    ],
    "page": 1,
    "page_size": 50,
    "total": 1
  }
  ```
- **Business rules:** `resource_key` is required; pagination defaults to page=1/page_size=50 (cap 200).
- **Errors:** `ERR_NO_SUCH_RESOURCE`, `ERR_INVALID_PAGINATION`, 401 unauthorized.

### Delete Quota Rule
- **Purpose:** remove enforcement/observation for a resource; only one rule exists per resource.
- **Request**
  ```http
  DELETE /v1/quota-rules/{ruleID}
  ```
- **Response**
  ```json
  { "status": "deleted" }
  ```
- **Business rules:** rule must belong to the authenticated account; deleting removes enforcement entirely.
- **Errors:** `ERR_RULE_NOT_FOUND`, 404 missing rule, 401 unauthorized.

## Quota Evaluation API
### Check Quota
- **Purpose:** preflight usage without consuming counters; ideal for gating UI and showing remaining balances.
- **Request**
  ```http
  POST /v1/quota/check

  {
    "resource_key": "apples-discard",
    "subject_id": "sub_1234",
    "amount": 0
  }
  ```
- **Response**
  ```json
  {
    "allowed": true,
    "remaining": 975,
    "limit": 1000
  }
  ```
- **Business rules:** `amount` ≥ 0 (use 0 for read-only peek); resource must have a quota rule; `non_enforced` rules still return remaining/limit; include `subject_id` for per-subject usage.
- **Errors:** `ERR_NO_QUOTA_RULE`, `ERR_INVALID_AMOUNT`, 400 invalid payload, 404 missing resource, 401 unauthorized.

### Consume Quota
- **Purpose:** record usage and enforce limits; provide idempotent `request_id` to avoid double-charging.
- **Request**
  ```http
  POST /v1/quota/consume

  {
    "resource_key": "apples-discard",
    "subject_id": "sub_1234",
    "amount": 25,
    "request_id": "unique-idempotency-key"
  }
  ```
- **Response**
  ```json
  {
    "allowed": true,
    "remaining": 950
  }
  ```
- **Business rules:** `amount` > 0; `request_id` required and reused for safe retries; `non_enforced` rules never block; enforced rules return `allowed=false` when limits would be exceeded; fails with `ERR_NO_QUOTA_RULE` if no rule exists.
- **Errors:** `ERR_INVALID_AMOUNT`, `ERR_QUOTA_CONSUME_FAILED`, `ERR_QUOTA_EXCEEDED`, 409 when `request_id` is replayed with different inputs, 404 missing resource, 401 unauthorized.

## What this devkit provides
- `examples/` — focused code snippets for core flows (register resources and quota rules, check vs. consume with idempotency, monitor-mode handling). How to run:
  - Set env vars: `BASE_URL=https://quota-api.thrysha.io` and `API_KEY=<your Quota API key>`.
  - Node.js: `node examples/node.js`
  - Python: `python examples/python.py` (requires `pip install requests`)
  - Go: `go run ./examples/go` (standard library only)
  - cURL: `./examples/curl.sh` (requires `jq`)
  - Each sample runs: create resource → create quota rule → check quota → consume quota (with idempotent `request_id`).
- `openapi/` — canonical OpenAPI definition (`spec.yaml`) for the Quota API.
- `postman/` — ready-to-import Postman/Hoppscotch collection (`thrysha.postman_collection.json`). To use:
  1) Install Postman (or Hoppscotch).
  2) Import the collection.
  3) Create an environment with `base_url` (e.g., `https://quota-api.thrysha.io`), `api_key` (your Quota API key), `resource_key`, `subject_id`, and optional `quota_rule_id`.
  4) Call “Create Resource” then “Create Quota Rule” (copy its `id` into `quota_rule_id` if you plan to delete it).
  5) Use “Check Quota” / “Consume Quota” with `resource_key` + `subject_id`; “List” endpoints work without extra setup.
- `references/` — conceptual docs (`concepts.md`, `overview.md`, `patterns.md`, `quickstart.md`) to explain Quota primitives, usage patterns, and integration guidance.

Use these directories together to explore the quota enforcement flow quickly, validate behavior, and share ready-to-run reference integrations with your team.
