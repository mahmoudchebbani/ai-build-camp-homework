import os
import urllib.request

import duckdb

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
PARQUET_FILE = "yellow_tripdata_2024-01.parquet"

con = duckdb.connect("taxi.db")


def setup_database():
    """Download the parquet file and load it into DuckDB."""
    if not os.path.exists(PARQUET_FILE):
        print(f"Downloading {DATA_URL}...")
        urllib.request.urlretrieve(DATA_URL, PARQUET_FILE)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS trips AS
        SELECT * FROM '{PARQUET_FILE}'
    """)
    count = con.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
    print(f"Loaded {count} rows")
    return count


class SQLTools:
    """Tools the agent uses to explore and query the trips table."""

    def __init__(self, connection=con, max_rows: int = 50):
        self.con = connection
        self.max_rows = max_rows

    def get_schema(self) -> str:
        """Get the column names and types of the trips table.

        Always call this first, before writing any SQL query.
        """
        rows = self.con.execute("DESCRIBE trips").fetchall()
        return "\n".join(f"{row[0]}: {row[1]}" for row in rows)

    def run_sql(self, query: str) -> str:
        """Run a SQL query against the DuckDB database and return the results.

        Args:
            query: A DuckDB SQL query. The table is called trips.

        Returns:
            Column headers followed by up to 50 data rows, one per line.
        """
        try:
            cursor = self.con.execute(query)
        except duckdb.Error as e:
            return f"Error: {e}"

        if cursor.description is None:
            return "Query executed, no rows returned."

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchmany(self.max_rows)

        lines = [" | ".join(columns)]
        lines += [" | ".join(str(value) for value in row) for row in rows]
        return "\n".join(lines)
