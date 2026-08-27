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

def validate_and_filter(requests: list[dict]) -> dict:
    seen_request = set()
    tenant_metrics = {}
    summary = {}
    dropped_deduplicates = 0
    top_tenant_by_bandwith = ""
    highest_total_bandwith = 0
    for req in requests:
        if req["request_id"] in seen_request: # Deduplication
            dropped_deduplicates+=1
            continue
        seen_request.add(req["request_id"])

        if req["tenant_id"] not in tenant_metrics:
            tenant_metrics[req["tenant_id"]] = {
                "total_requests": 0,
                "total_mb": 0.0000,
                "error_rate": 0.0,
                "endpoints_hit": set()
            }

        entry = tenant_metrics[req["tenant_id"]]

        # Total request
        entry["total_requests"]+=1

        # Total mb and highest bandwith
        entry["total_mb"] += (req["bytes"] / (1024*1024))
        if highest_total_bandwith < entry["total_mb"]:
            highest_total_bandwith = entry["total_mb"]
            top_tenant_by_bandwith = req["tenant_id"]

        # Error rate
        entry["error_rate"] += 1 if req["status_code"] >= 400 else 0

        # Endpoints
        entry["endpoints_hit"].add(req["endpoint"])

    for tenant in tenant_metrics:
        tenant_metrics[tenant]["total_mb"] = round(tenant_metrics[tenant]["total_mb"], 4)
        tenant_metrics[tenant]["error_rate"] = round((tenant_metrics[tenant]["error_rate"] / tenant_metrics[tenant]["total_requests"]) * 100, 2)
        tenant_metrics[tenant]["endpoints_hit"] = sorted(tenant_metrics[tenant]["endpoints_hit"])

    # Global Summary
    summary["total_tenants"] = len(tenant_metrics)
    summary["dropped_duplicates"] = dropped_deduplicates
    summary["top_tenant_by_bandwidth"] = top_tenant_by_bandwith

    return summary | {"tenant_metrics": tenant_metrics}

if __name__ == "__main__":
    print(validate_and_filter(raw_requests))