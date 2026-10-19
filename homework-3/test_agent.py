import re

import pytest

from judge import assert_criteria
from sql_agent import sql_agent
from sql_tools import setup_database
from utils import collect_tools

setup_database()


def normalize(text: str) -> str:
    """Drop thousands separators so 22,413 and 22413 both match."""
    return text.replace(",", "")


@pytest.mark.asyncio
async def test_trips_with_more_than_5_passengers():
    result = await sql_agent.run("How many trips had more than 5 passengers?")
    output = result.output

    assert isinstance(output.sql_query, str)
    assert output.sql_query.strip() != ""

    # SELECT COUNT(*) FROM trips WHERE passenger_count > 5
    assert "22413" in normalize(output.result_text)


@pytest.mark.asyncio
async def test_agent_gets_schema_before_running_sql():
    result = await sql_agent.run("What is the most common payment type?")

    tool_calls = collect_tools(result.new_messages())
    names = [call.name for call in tool_calls]
    print("tool calls:", names)

    assert names[0] == "get_schema"
    assert "run_sql" in names


@pytest.mark.asyncio
async def test_hour_with_highest_average_fare():
    result = await sql_agent.run("Which hour of the day has the highest average fare amount?")
    print("agent output:", result.output)

    await assert_criteria(result, [
        "the SQL query correctly calculates average fare by hour of day",
        "the result identifies a specific hour as having the highest average fare",
        "the result includes the actual average fare amount",
    ])


def contains_number(text: str, expected: float, tolerance: float = 0.01) -> bool:
    """True if any number in the text is within tolerance of the expected value."""
    numbers = re.findall(r"\d+(?:\.\d+)?", normalize(text))
    return any(abs(float(n) - expected) <= tolerance for n in numbers)


# question, columns the SQL must use, check on result_text
# expected values come from running the queries directly in DuckDB
SCENARIOS = [
    pytest.param(
        "What is the average tip amount for credit card payments?",
        ["tip_amount", "payment_type"],
        lambda text: contains_number(text, 4.17),  # payment_type = 1 -> 4.1697
        id="avg-tip-credit-card",
    ),
    pytest.param(
        "Which pickup location (PULocationID) has the most trips?",
        ["pulocationid"],
        lambda text: "132" in text,  # 145,240 trips
        id="top-pickup-location",
    ),
    pytest.param(
        "What is the average fare for trips longer than 10 miles?",
        ["fare_amount", "trip_distance"],
        lambda text: contains_number(text, 62.88),  # 62.8808
        id="avg-fare-over-10-miles",
    ),
    pytest.param(
        "How many trips had zero passengers recorded?",
        ["passenger_count"],
        lambda text: "31465" in normalize(text),
        id="zero-passengers",
    ),
    pytest.param(
        "What is the busiest day of the week for taxi trips?",
        ["tpep_pickup_datetime"],
        lambda text: "wednesday" in text.lower(),  # 495,032 trips
        id="busiest-day-of-week",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("question, columns, check_result", SCENARIOS)
async def test_more_questions(question, columns, check_result):
    result = await sql_agent.run(question)
    output = result.output
    print("agent output:", output)

    names = [call.name for call in collect_tools(result.new_messages())]
    assert names[0] == "get_schema"
    assert "run_sql" in names

    sql = output.sql_query.lower()
    for column in columns:
        assert column in sql, f"expected {column} in {output.sql_query}"

    assert check_result(output.result_text), output.result_text
