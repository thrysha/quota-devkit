# Usage Patterns

## Per-user or per-tenant limits
Create a resource per user or per tenant, then assign a rule with a fixed window (e.g., daily limits).

## API call metering
Use a shared resource for an endpoint or feature. Check before compute, consume after success.

## Billing enforcement
Combine per-resource tracking with the `/v1/summary` endpoint to monitor usage over billing periods.

## Graceful degradation
Use `monitor_only` rules to observe usage without blocking. Switch to `enforced` when ready.

## Retry-safe operations
Always include a stable `request_id` when consuming quota to avoid double counting. This is suitable for queues, workers, and serverless functions.

## Free-tier implementation
Assign low daily or monthly limits to free users, and higher limits to paid plans by adjusting the rule’s quota_limit and reset_window_seconds.

