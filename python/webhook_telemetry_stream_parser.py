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
    "valid_records": 6,
    "corrupted_records": 4,
    "critical_incidents": 2,
    "total_latency_seconds": 5.5507, # (150.5 + 2500.0 + 1200.0 + 80.2 + 1500.0 + 120.0 - check validity) -> calculated based on 5 valid entries
    "average_latency_ms": 925.12 # Average across valid records rounded to 2 decimal places
}

def validate_and_filter(records: list[str]) -> tuple[list[str], int, int]:
    records_copy = records.copy()
    corrupted_count = 0
    critical_count = 0
    for idx in range(len(records_copy)-1, -1, -1): # Start from end since pop shifts the index
        record = records_copy[idx].split("|")
        # Validate
        if len(record) != 5: 
            records_copy[idx] = "corrupted"
            corrupted_count+=1
            continue 
        elif record[1] == "unknown" or record[1] == "": 
            records_copy.pop(idx) 
            corrupted_count+=1
            continue
        # Filter
        for val in record:
            if isinstance(val, str):
                val.strip()
        # Type Cast
        record[2], record[3] = int(record[2]), float(record[3])
        record[4] = bool(record[4]) if record[4] == "true" or record[4] == "1" else bool("")
        if record[1] == "auth-service" and (record[2] >= 500 or record[3] > 1000.0):
            critical_count+=1
        records_copy[idx] = record # Update
    return records_copy, corrupted_count, critical_count

def process_records(orig_records: list[str], filtered_records: list[str], corrupted_count: int, critical_count: int) -> dict[str, int | float]:
    total_ms = sum([record[3] for record in filtered_records if isinstance(record[3], float)])
    metrics = {
        "total_raw_records": len(orig_records),
        "valid_records": len(orig_records) - corrupted_count,
        "corrupted_records": corrupted_count,
        "critical_incidents": critical_count,
        "total_latency_seconds": total_ms / 1000, # (total_ms / 1000) 
        "average_latency_ms": round(total_ms / len(filtered_records), 2)
    }
    return metrics

if __name__ == "__main__":
    filtered_records, corrupted_count, critical_count = validate_and_filter(raw_stream)
    print(process_records(raw_stream, filtered_records, corrupted_count, critical_count))