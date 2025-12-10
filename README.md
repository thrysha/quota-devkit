# Thrysha Devkit

Developer toolkit for integrating with the Thrysha API. This repo bundles runnable examples, the OpenAPI spec, a Postman collection, and reference docs.

## What's inside
- `examples/` — focused code snippets for core flows (resource + quota create/check/consume).
- `openapi/` — canonical OpenAPI spec (`spec.yaml`) for the Thrysha API.
- `postman/` — Postman collection for the core endpoints.
- `references/` — concepts, patterns, and quickstart docs.

## Getting started
1. Clone and `cd thrysha-devkit`.
2. Export `BASE_URL` (e.g., `https://api.thrysha.com`) and `API_KEY` (your Thrysha API key).
3. Import the Postman collection (`postman/thrysha.postman_collection.json`) or browse the OpenAPI spec (`openapi/spec.yaml`).
4. Run a language example from `examples/` to exercise the core flow.

### Running the examples
- Export `BASE_URL` (e.g., `https://api.thrysha.com`) and `API_KEY` (your Thrysha API key).
- Node: `node examples/node.js`
- Python: `python examples/python.py` (requires `pip install requests`)
- Go: `go run ./examples/go`
- cURL: `./examples/curl.sh` (requires `jq`)

## Contributing
- Keep examples small and runnable.
- Update the OpenAPI spec and Postman collection when endpoints change.
- Document prerequisites (API keys, env vars, tooling versions) in each folder's README.
