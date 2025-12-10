# Postman / Hoppscotch Collections

- `thrysha.postman_collection.json` — main Postman collection.

Tip: keep IDs stable so diffs stay readable in PRs.

## How to use
1) Install Postman (or Hoppscotch) locally.
2) Import `thrysha.postman_collection.json`.
3) Create an environment with:
   - `base_url` (e.g., `https://api.thrysha.com`)
   - `api_key` (your Thrysha API key)
   - Optional: `resource_id`, `quota_rule_id` to speed up delete/check calls.
4) Call “Create Resource” → copy its `id` into the environment’s `resource_id`.
5) Call “Create Quota Rule” → copy its `id` into `quota_rule_id` if you plan to delete it.
6) Use “Check Quota” / “Consume Quota” with those IDs; “List” endpoints work without extra setup.
