package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
)

func main() {
	base := os.Getenv("BASE_URL")
	key := os.Getenv("API_KEY")
	if base == "" || key == "" {
		log.Fatal("Set BASE_URL and API_KEY env vars to run the example.")
	}

	client := &http.Client{Timeout: 10 * time.Second}
	headers := map[string]string{
		"Content-Type":  "application/json",
		"Authorization": fmt.Sprintf("Bearer %s", key),
	}

	// 1) Create resource
	resourceName := fmt.Sprintf("example-resource-%d", time.Now().Unix())
	resource := mustPost(client, base+"/v1/resources", headers, map[string]any{
		"name":        resourceName,
		"description": "example",
	})
	fmt.Printf("Resource created: %s\n", toJSON(resource))

	// 2) Create quota rule
	mustPost(client, base+"/v1/quota-rules", headers, map[string]any{
		"resource_id":          resource["id"],
		"quota_policy":         "limited",
		"quota_limit":          100,
		"reset_strategy":       "fixed_window",
		"reset_window_seconds": 86400,
		"enforcement_mode":     "enforced",
	})
	fmt.Println("Quota rule created")

	// 3) Check quota
	check := mustPost(client, base+"/v1/quota/check", headers, map[string]any{
		"resource_id": resource["id"],
		"amount":      1,
	})
	fmt.Printf("Check response: %s\n", toJSON(check))

	// 4) Consume quota
	consume := mustPost(client, base+"/v1/quota/consume", headers, map[string]any{
		"resource_id": resource["id"],
		"amount":      1,
		"request_id":  fmt.Sprintf("req-%d", rand.Int63()),
	})
	fmt.Printf("Consume response: %s\n", toJSON(consume))
}

func mustPost(client *http.Client, url string, headers map[string]string, payload map[string]any) map[string]any {
	body, err := json.Marshal(payload)
	if err != nil {
		log.Fatalf("marshal payload: %v", err)
	}

	req, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		log.Fatalf("build request: %v", err)
	}
	for k, v := range headers {
		req.Header.Set(k, v)
	}

	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		data, _ := io.ReadAll(resp.Body)
		log.Fatalf("%s: %s", resp.Status, string(data))
	}

	var out map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		log.Fatalf("decode response: %v", err)
	}
	return out
}

func toJSON(v any) string {
	b, _ := json.MarshalIndent(v, "", "  ")
	return string(b)
}
