# Examples

Focused code snippets for common flows:
- Register resources and quota rules
- Check vs. consume with idempotency
- Monitor-mode handling (log-only)

## Running the API flow samples
All examples assume two env vars:
- `BASE_URL` — e.g., `https://api.thrysha.com`
- `API_KEY` — your Thrysha API key

Examples available:
- Node.js: `node examples/node.js`
- Python: `python examples/python.py` (requires `pip install requests`)
- Go: `go run ./examples/go` (uses only the standard library)
- cURL: `./examples/curl.sh` (requires `jq`)

Each sample performs: create resource -> create quota rule -> check quota -> consume quota (with idempotent `request_id`).
