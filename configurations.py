configurations = {
    "Baseline": [
        "ALTER SYSTEM SET shared_buffers = '128kB';",
        "ALTER SYSTEM SET work_mem = '64MB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 2;",
    ],
}
