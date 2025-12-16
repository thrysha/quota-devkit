# Postman / Hoppscotch Collections

- `thrysha.postman_collection.json` — main Postman collection for the Quota API.

Tip: keep IDs stable so diffs stay readable in PRs.

## How to use
1) Install Postman (or Hoppscotch) locally.
2) Import `thrysha.postman_collection.json`.
3) Create an environment with:
   - `base_url` (e.g., `https://quota-api.thrysha.io`)
   - `api_key` (your Quota API key)
   - `resource_key` (set to the handle you create)
   - `subject_id` (any subject under that resource)
   - Optional: `quota_rule_id` to speed up deletes.
4) Call “Create Resource” → it uses `resource_key`.
5) Call “Create Quota Rule” → copy its `id` into `quota_rule_id` if you plan to delete it.
6) Use “Check Quota” / “Consume Quota” with `resource_key` and `subject_id`; “List” endpoints work without extra setup.
