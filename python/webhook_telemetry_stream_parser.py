# Scenario
# You are building the raw ingestion engine for an API gateway monitoring service. 
# The gateway outputs raw, pipe-delimited log strings from a high-throughput stream. 
# Your job is to process this raw stream using only fundamental variables, loops, and control flow to generate a structured metric summary.

# <timestamp>|<service_name>|<http_status>|<latency_ms>|<is_retry>
raw_stream = [
    "2026-08-23T09:00:00Z|auth-service|200|150.5|false",
    "2026-08-23T09:00:01Z|payment-api|500|2500.0|true",
    "INVALID_STREAM_LINE_NO_PIPES",
    "2026-08-23T09:00:02Z|auth-service|503|1200.0|false",
    "2026-08-23T09:00:03Z||200|45.0|false",
    "2026-08-23T09:00:04Z|order-service|200|80.2|0",
    "2026-08-23T09:00:05Z|auth-service|200|1500.0|1",
    "2026-08-23T09:00:06Z|unknown|200|30.0|false",
    "2026-08-23T09:00:07Z|payment-api|404|120.0|false",
    "2026-08-23T09:00:08Z|order-service|500|850.5|true|EXTRA_FIELD"
]

# Expected Output
{
    "total_raw_records": 10,
    "valid_records": 5,
    "corrupted_records": 5,
    "critical_incidents": 2,
    "total_latency_seconds": 4.3507, # (150.5 + 2500.0 + 1200.0 + 80.2 + 1500.0 + 120.0 - check validity) -> calculated based on 5 valid entries
    "average_latency_ms": 1090.14 # Average across valid records rounded to 2 decimal places
}

def validate_and_filter(records: list[str]) -> list[str]:
    records_copy = records.copy()
    for idx in range(len(records_copy)-1, -1, -1): # Start from end since pop shifts the index
        record = records_copy[idx].split("|")
        # Validate
        if len(record) != 5: 
            records_copy[idx] = "corrupted"
            continue 
        elif record[1] == "unknown": 
            records_copy.pop(idx) 
            continue
        # Filter
        for val in record:
            if isinstance(val, str):
                val.strip()
        # Type Cast
        record[2], record[3] = int(record[2]), float(record[3])
        record[4] = bool(record[4]) if record[4] == "true" or record[4] == "1" else bool("")
    return records_copy

if __name__ == "__main__":
    print(validate_and_filter(raw_stream))