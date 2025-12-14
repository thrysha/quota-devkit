# Key Concepts

## Resource
A resource is a named entity representing a limited or billable action. Examples include API calls, AI inferences, feature usage, or per-customer operations.

Each resource:
- Belongs to an account
- Has a unique name per account
- Can have at most one active quota rule

## Quota Rule
Defines how usage is tracked and enforced.

Fields:
- `quota_policy` (limited or unlimited)
- `quota_limit` for limited rules
- `reset_strategy` (unit + interval: hour, day, week, month, year, never)
- `enforcement_mode` (enforced or non_enforced/monitor-only)

## Check vs Consume
- **Check** evaluates whether an action would be allowed without consuming usage.
- **Consume** records usage and enforces the limit. It is idempotent when the same `request_id` is reused.

## Reset Strategies
- **hour/day/week/month/year**: fixed windows aligned to UTC boundaries (hour at :00, day at 00:00, week at Monday 00:00, month on the 1st, year on Jan 1). `interval` lets you step in whole multiples (e.g., every 2 hours).
- **never**: total lifetime counter (no reset).

## Idempotency
`request_id` ensures retries do not double-consume usage, which is crucial for distributed systems and flaky networks.
