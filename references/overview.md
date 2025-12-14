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
- Fixed windows only: `reset_strategy` is `{ "unit": "hour|day|week|month|year|never", "interval": N }`, aligned to UTC boundaries (hour at :00, day at 00:00, week Monday 00:00, month on the 1st, year on Jan 1). `interval` lets you step in whole multiples (e.g., every 2 hours).
- “never” disables resets.

### Persistence guarantees
- Enforcement counters live in Redis with TTLs set to the current window. If Redis is empty but the snapshot/state store is configured, the first check/consume rehydrates from durable state; otherwise counters restart at zero.
- Usage history for summaries is persisted separately. Without Redis persistence (AOF/RDB), a Redis crash can drop up to roughly `snapshot interval + current window` of usage; both enforcement and billing effectively forgive that interval. Enabling Redis persistence or shortening the snapshot interval reduces exposure.
- All enforcement and idempotency are scoped to `(resource_id, subject_id)` so subjects do not interfere with each other.
