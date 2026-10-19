# Homework 3: Testing a DuckDB SQL Agent

A PydanticAI agent that answers questions about the NYC Yellow Taxi January 2024 data by writing SQL against DuckDB, plus a pytest suite that checks its answers, its tool calls and its cost.

- **Framework:** PydanticAI
- **LLM provider:** OpenAI (`gpt-4o-mini`)

## Setup

```bash
cd homework-3
uv sync
cp .env.example .env   # then add your OpenAI key
```

The first run downloads the parquet file (~47 MB) and loads it into `taxi.db`.

## Files

| File | What it does |
| --- | --- |
| `sql_tools.py` | `setup_database()` loads the data; `SQLTools` has `get_schema()` and `run_sql(query)` (max 50 rows) |
| `sql_agent.py` | `SQLResult` model and the agent; run it and type a question |
| `utils.py` | `collect_tools` pulls tool calls out of the agent's messages |
| `judge.py` | LLM judge: `evaluate_agent_performance` and `assert_criteria` |
| `test_agent.py` | 8 tests: exact answers, tool order, LLM judge, 5 parametrized scenarios |
| `cost_tracker.py`, `patch_agent.py`, `conftest.py` | Record token usage of every agent run and print the total cost after the suite |

```bash
uv run python sql_agent.py
uv run pytest -v
```

## Answers

| # | Question | Answer |
| --- | --- | --- |
| 1 | Rows in the January 2024 dataset | 2,964,624 |
| 2 | Average trip distance for rides with 2 passengers | 3.78 |
| 3 | Trips with more than 5 passengers | 22,413 |
| 4 | Second tool the agent calls | `run_sql` |
| 5 | Hour with the highest average fare | 5 (about $26.62) |
| 6 | Column to filter for zero passengers | `passenger_count` |
| 7 | Total cost of the test suite (bonus) | Less than $0.05 (about $0.002) |

### Q6 scenarios

Expected values come from running the queries directly in DuckDB.

| Question | Columns in the SQL | Expected value |
| --- | --- | --- |
| Average tip for credit card payments | `tip_amount`, `payment_type` | $4.17 (`payment_type = 1`) |
| Pickup location with the most trips | `PULocationID` | 132 (145,240 trips) |
| Average fare for trips over 10 miles | `fare_amount`, `trip_distance` | $62.88 |
| Trips with zero passengers | `passenger_count` | 31,465 |
| Busiest day of the week | `tpep_pickup_datetime` | Wednesday (495,032 trips) |

Every scenario also checks that `get_schema` is called before `run_sql`.

## Notes

- The agent is created once at import, so all async tests share one event loop (`asyncio_default_test_loop_scope = "session"` in `pyproject.toml`). Without it the second test fails with `Event loop is closed`.
- The schema doesn't say that credit card is `payment_type = 1`; `gpt-4o-mini` knows the TLC codes. A data dictionary in the instructions would make that less fragile.
