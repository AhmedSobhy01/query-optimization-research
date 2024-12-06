configurations = {
    "Baseline": [
        "ALTER SYSTEM SET shared_buffers = '1GB';",
        "ALTER SYSTEM SET work_mem = '16MB';",
        "ALTER SYSTEM SET effective_cache_size = '4GB';",
        "ALTER SYSTEM SET maintenance_work_mem = '512GB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 2;",
    ],
    "High Memory": [
        "ALTER SYSTEM SET shared_buffers = '2GB';",
        "ALTER SYSTEM SET work_mem = '32MB';",
        "ALTER SYSTEM SET effective_cache_size = '6GB';",
        "ALTER SYSTEM SET maintenance_work_mem = '1GB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 4;",
    ],
}
