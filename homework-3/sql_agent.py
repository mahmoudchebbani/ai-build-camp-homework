from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel  # noqa: E402
from pydantic_ai import Agent  # noqa: E402

from sql_tools import SQLTools, setup_database  # noqa: E402


class SQLResult(BaseModel):
    sql_query: str
    result_text: str
    row_count: int


instructions = """
You're a data analyst answering questions about NYC Yellow Taxi trips from January 2024.
The data is in a DuckDB table called trips.

Always start by calling get_schema to see the columns and their types,
before running any queries. Then write a DuckDB SQL query and run it with run_sql.

In the output, put the final SQL query you ran in sql_query, a short answer to
the question in result_text, and the number of rows the query returned in row_count.
""".strip()

sql_tools = SQLTools()

sql_agent = Agent(
    "openai:gpt-4o-mini",
    instructions=instructions,
    output_type=SQLResult,
    tools=[sql_tools.get_schema, sql_tools.run_sql],
)


def tool_calls(result):
    calls = []
    for message in result.all_messages():
        for part in message.parts:
            if part.part_kind == "tool-call":
                calls.append((part.tool_name, part.args))
    return calls


if __name__ == "__main__":
    setup_database()
    question = input("Question: ").strip() or "What's the average trip distance for rides with 2 passengers?"
    result = sql_agent.run_sync(question)
    for name, args in tool_calls(result):
        print(f"TOOL {name}({args})")
    print(result.output.model_dump_json(indent=2))
    print(result.usage)
