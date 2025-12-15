# Overview

The Thrysha API provides a simple way to enforce usage limits, track consumption, and prevent abuse across APIs and features. It is designed for multi-tenant applications that need predictable limits, transparent reset windows, and idempotent consumption.

A resource represents any billable or limited action. Each resource may have a single quota rule defining its policy, reset strategy, and enforcement mode.

Core endpoints:
- `/v1/resources` for creating, listing, and deleting resources
- `/v1/quota-rules` for attaching quota rules to resources
- `/v1/quota/check` to evaluate a request without consuming usage (requires `subject_id` to scope per subject)
- `/v1/quota/consume` to record usage with idempotency (requires `subject_id`; returns `allowed=false` on enforced limit breaches with HTTP 200)

The API uses API-key authentication for runtime quota calls and Firebase authentication for account-level operations such as managing API keys.

### Reset windows
- Fixed windows only: `reset_strategy` is `{ "unit": "hour|day|week|month|year|never", "interval": N }`, aligned to UTC boundaries (hour at :00, day at 00:00, week Monday 00:00, month on the 1st, year on Jan 1). `interval` lets you step in whole multiples (e.g., every 2 hours) and is capped to at most one year of duration (hour ≤ 8,760; day ≤ 365; week ≤ 52; month ≤ 12; year interval ≤ 1).
- “never” disables resets.

### Resource keys
- Requests use `resource_key` as the handle (responses still include `resource_id`). Keys must match `^[a-z0-9][a-z0-9_-]{1,62}$` and are unique per account (case-insensitive). Provide a separate description for display.

### Persistence guarantees
- Enforcement counters live in Redis with TTLs set to the current window. Redis readiness is health-gated; if Redis is unhealthy/empty, check/consume return 503 and snapshotting pauses until a bulk hydrate restores counters from durable state. Use AOF (e.g., `appendfsync everysec`) to avoid cold starts.
- Usage history for summaries is persisted separately. Without Redis persistence, a Redis crash can drop up to roughly `snapshot interval + current window` of usage; both enforcement and billing effectively forgive that interval. Persistence or shorter snapshot intervals reduce exposure.
- All enforcement and idempotency are scoped to `(resource_key, subject_id)` so subjects do not interfere with each other.
