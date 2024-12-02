import psycopg2
from psycopg2.extras import DictCursor
import time
import csv
import os
from queries import queries
from configurations import configurations
from indexes import indexes
import subprocess

DB_PARAMS = {
    "dbname": "stats_performance_test",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5444,
}

RUNS_PER_QUERY = 35
RESULTS_FILE = "experiment_results.csv"

POSTGRES_BIN_PATH = r"C:\Program Files\PostgreSQL\17\bin"
POSTGRES_DATA_PATH = r"C:\Program Files\PostgreSQL\17\data"


def vacuum_database():
    conn = psycopg2.connect(**DB_PARAMS)
    conn.set_session(autocommit=True)
    with conn.cursor() as cur:
        cur.execute("VACUUM FULL;")
    conn.commit()
    conn.close()


def restart_postgres():
    if os.name == "nt":
        subprocess.run(
            f'"{POSTGRES_BIN_PATH}\\pg_ctl.exe" restart -D "{POSTGRES_DATA_PATH}"',
            shell=True,
            check=True,
        )
    else:
        os.system("sudo systemctl restart postgresql")


def clear_cache():
    with psycopg2.connect(**DB_PARAMS) as conn:
        conn.set_session(autocommit=True)
        with conn.cursor() as cur:
            cur.execute("SELECT pg_stat_reset();")
            cur.execute("DISCARD ALL;")
        conn.commit()

    if os.name != "nt":
        os.system("sudo sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
        print("System cache cleared.")


def execute_query(conn, query, clear_caches=True):
    if clear_caches:
        clear_cache()

    with conn.cursor(cursor_factory=DictCursor) as cur:
        start_time = time.time()
        cur.execute(query)
        conn.commit()
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        return execution_time


def run_experiments():
    file_exists = os.path.isfile(RESULTS_FILE)

    vacuum_database()

    with open(RESULTS_FILE, "a", newline="") as csvfile:
        fieldnames = [
            "#",
            "RunNumber",
            "ExecutionTime_ms",
            "Configuration",
            "IndexStrategy",
            "DataSetSize",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for config_name, config_commands in configurations.items():
            print(f"Applying configuration: {config_name}")
            apply_configuration(config_commands)

            for index_name, index_commands in indexes.items():
                print(f"Using index strategy: {index_name}")
                reset_indexes()
                create_indexes(index_commands)

                for index, query in queries.items():
                    print(f"Executing Query {index}")
                    for run in range(1, RUNS_PER_QUERY + 1):
                        conn = psycopg2.connect(**DB_PARAMS)
                        execution_time = execute_query(conn, query)
                        conn.close()

                        writer.writerow(
                            {
                                "#": index,
                                "RunNumber": run,
                                "ExecutionTime_ms": execution_time,
                                "Configuration": config_name,
                                "IndexStrategy": index_name,
                                "DataSetSize": DATASET_SIZE,
                            }
                        )
                        print(
                            f"Query {index}, Run {run}, Time: {execution_time:.2f} ms"
                        )

    print("Experiments completed.")


def apply_configuration(config_commands):
    conn = psycopg2.connect(**DB_PARAMS)
    conn.set_session(autocommit=True)
    with conn.cursor() as cur:
        for command in config_commands:
            cur.execute(command)
    conn.commit()
    conn.close()

    restart_postgres()


def reset_indexes():
    conn = psycopg2.connect(**DB_PARAMS)
    with conn.cursor() as cur:
        drop_index_query = """
        SELECT 'DROP INDEX ' || quote_ident(indexname) || ';'
        FROM pg_indexes
        WHERE schemaname = 'public' AND indexname NOT LIKE 'pg_%' AND indexname NOT LIKE '%_pkey';
        """
        cur.execute(drop_index_query)
        drop_commands = cur.fetchall()
        for cmd in drop_commands:
            cur.execute(cmd[0])
    conn.commit()
    conn.close()


def create_indexes(index_commands):
    conn = psycopg2.connect(**DB_PARAMS)
    with conn.cursor() as cur:
        for command in index_commands:
            cur.execute(command)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    DATASET_SIZE = "Medium"

    run_experiments()
