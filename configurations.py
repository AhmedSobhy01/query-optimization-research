configurations = {
    "Baseline": [
        "ALTER SYSTEM SET work_mem = '4MB';",
        "ALTER SYSTEM SET effective_cache_size = '4GB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 2;",
        "ALTER SYSTEM SET random_page_cost  = 4.0;",
        "ALTER SYSTEM SET maintenance_work_mem = '64MB';",
    ],
    
    "FirstArr": [
        "ALTER SYSTEM SET work_mem = '16MB';",
        "ALTER SYSTEM SET effective_cache_size = '8GB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 2;",
        "ALTER SYSTEM SET random_page_cost  = 2.0;",
        "ALTER SYSTEM SET maintenance_work_mem = '128MB';",
    ],
    "SecondArr": [
        "ALTER SYSTEM SET work_mem = '256MB';",
        "ALTER SYSTEM SET effective_cache_size = '8GB';",
        "ALTER SYSTEM SET max_parallel_workers_per_gather = 8;",
        "ALTER SYSTEM SET random_page_cost  = 1.1;",
        "ALTER SYSTEM SET maintenance_work_mem = '1GB';",
    ],

}
