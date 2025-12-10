// Minimal Node.js example for Thrysha API
// Requires Node 18+ (built-in fetch and crypto.randomUUID).

const base = process.env.BASE_URL;
const key = process.env.API_KEY;

if (!base || !key) {
  console.error("Set BASE_URL and API_KEY env vars to run the example.");
  process.exit(1);
}

function authHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${key}`,
  };
}

async function request(path, options) {
  const res = await fetch(`${base}${path}`, options);
  const text = await res.text();
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return text ? JSON.parse(text) : {};
}

async function main() {
  const resourceName = `example-resource-${Date.now()}`;

  // 1) Create resource
  const resource = await request("/v1/resources", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ name: resourceName, description: "example" }),
  });
  console.log("Resource created:", resource);

  // 2) Create quota rule
  await request("/v1/quota-rules", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      resource_id: resource.id,
      quota_policy: "limited",
      quota_limit: 100,
      reset_strategy: "fixed_window",
      reset_window_seconds: 86400,
      enforcement_mode: "enforced",
    }),
  });
  console.log("Quota rule created");

  // 3) Check quota
  const check = await request("/v1/quota/check", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ resource_id: resource.id, amount: 1 }),
  });
  console.log("Check response:", check);

  // 4) Consume quota
  const consume = await request("/v1/quota/consume", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      resource_id: resource.id,
      amount: 1,
      request_id: crypto.randomUUID(),
    }),
  });
  console.log("Consume response:", consume);
}

main().catch((err) => {
  console.error("Example failed:", err.message);
  process.exit(1);
});
