# Overview

The Thrysha API provides a simple way to enforce usage limits, track consumption, and prevent abuse across APIs and features. It is designed for multi-tenant applications that need predictable limits, transparent reset windows, and idempotent consumption.

A resource represents any billable or limited action. Each resource may have a single quota rule defining its policy, reset strategy, and enforcement mode.

Core endpoints:
- `/v1/resources` for creating, listing, and deleting resources
- `/v1/quota-rules` for attaching quota rules to resources
- `/v1/quota/check` to evaluate a request without consuming usage
- `/v1/quota/consume` to record usage with idempotency

The API uses API-key authentication for runtime quota calls and Firebase authentication for account-level operations such as managing API keys.
