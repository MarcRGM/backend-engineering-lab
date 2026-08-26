# You are building an in-memory aggregation worker for a SaaS API platform. 
# The gateway emits batched request logs. 
# Multiple requests may arrive with duplicate request_id values due to network retries; 
# your system must enforce idempotency (process only the first occurrence of each request_id).

# You must ingest the raw event list, deduplicate records in O(1), 
# and generate a structured billing and usage report grouped per tenant.

raw_requests = [
    {"request_id": "req-001", "tenant_id": "tenant-a", "endpoint": "/api/v1/users", "status_code": 200, "bytes": 1048576},
    {"request_id": "req-002", "tenant_id": "tenant-b", "endpoint": "/api/v1/auth",  "status_code": 401, "bytes": 512000},
    {"request_id": "req-001", "tenant_id": "tenant-a", "endpoint": "/api/v1/users", "status_code": 200, "bytes": 1048576},  # Duplicate
    {"request_id": "req-003", "tenant_id": "tenant-a", "endpoint": "/api/v1/orders", "status_code": 500, "bytes": 2097152},
    {"request_id": "req-004", "tenant_id": "tenant-b", "endpoint": "/api/v1/users", "status_code": 200, "bytes": 1048576},
    {"request_id": "req-005", "tenant_id": "tenant-c", "endpoint": "/api/v1/health", "status_code": 200, "bytes": 256},
    {"request_id": "req-002", "tenant_id": "tenant-b", "endpoint": "/api/v1/auth",  "status_code": 401, "bytes": 512000},  # Duplicate
    {"request_id": "req-006", "tenant_id": "tenant-a", "endpoint": "/api/v1/auth",  "status_code": 200, "bytes": 1024},
]

# Expected Output
{
    "summary": {
        "total_tenants": 3,
        "dropped_duplicates": 2,
        "top_tenant_by_bandwidth": "tenant-a"
    },
    "tenant_metrics": {
        "tenant-a": {
            "total_requests": 3,
            "total_mb": 3.001,
            "error_rate": 33.33,
            "endpoints_hit": ["/api/v1/auth", "/api/v1/orders", "/api/v1/users"]
        },
        "tenant-b": {
            "total_requests": 2,
            "total_mb": 1.4883,
            "error_rate": 50.0,
            "endpoints_hit": ["/api/v1/auth", "/api/v1/users"]
        },
        "tenant-c": {
            "total_requests": 1,
            "total_mb": 0.0002,
            "error_rate": 0.0,
            "endpoints_hit": ["/api/v1/health"]
        }
    }
}

def validate_and_filter(requests: list[dict]) -> list[dict]:
    seen_request = set()
    tenant_metrics = {}
    dropped_deduplicates = 0
    for req in requests:
        if req["request_id"] in seen_request: # Deduplication
            dropped_deduplicates+=1
            continue
        seen_request.add(req["request_id"])
        tenant_metrics.setdefault(req["tenant_id"], {})
        tenant_metrics[req["tenant_id"]].setdefault("total_requests", 0)
        tenant_metrics[req["tenant_id"]]["total_requests"]+=1
        tenant_metrics[req["tenant_id"]].setdefault("total_mb", 0)
        tenant_metrics[req["tenant_id"]]["total_mb"]+= req["bytes"]
    return tenant_metrics

if __name__ == "__main__":
    print(validate_and_filter(raw_requests))