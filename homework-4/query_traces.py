import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from logfire.query_client import LogfireQueryClient

load_dotenv()

client = LogfireQueryClient(read_token=os.environ['LOGFIRE_READ_TOKEN'])


def query(sql):
    since = datetime.now(timezone.utc) - timedelta(days=7)
    return client.query_json_rows(sql=sql, min_timestamp=since)['rows']


if __name__ == "__main__":
    sessions = query("""
        SELECT trace_id, start_timestamp, duration
        FROM records
        WHERE span_name = 'trivia_session'
        ORDER BY start_timestamp DESC
    """)

    print("trivia_session traces (newest first):")
    for row in sessions:
        print(row['trace_id'], row['start_timestamp'], f"{row['duration']:.1f}s")

    for row in sessions:
        runs = query(f"""
            SELECT count(*) AS runs
            FROM records
            WHERE trace_id = '{row['trace_id']}' AND span_name = 'invoke_agent agent'
        """)
        print(row['trace_id'], "agent runs inside:", runs[0]['runs'])
