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
- `reset_strategy` (rolling_window, fixed_window, or no_reset)
- `reset_window_seconds` for windowed strategies
- `enforcement_mode` (enforced or monitor_only)

## Check vs Consume
- **Check** evaluates whether an action would be allowed without consuming usage.
- **Consume** records usage and enforces the limit. It is idempotent when the same `request_id` is reused.

## Reset Strategies
- **fixed_window**: resets at consistent intervals (e.g., daily, hourly)
- **rolling_window**: availability depends on the last N seconds of activity
- **no_reset**: total lifetime counter

## Idempotency
`request_id` ensures retries do not double-consume usage, which is crucial for distributed systems and flaky networks.

