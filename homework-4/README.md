# Homework 4: Monitoring a Trivia Agent with Logfire

A PydanticAI trivia quizmaster that fetches questions from the [Open Trivia DB](https://opentdb.com/), instrumented with Logfire. Each session is grouped under one span, and the traces are pulled back with the Logfire query client to rebuild runs and calculate cost.

- **Framework:** PydanticAI
- **LLM provider:** OpenAI (`gpt-4o-mini`)
- **Observability:** Logfire

## Setup

```bash
cd homework-4
uv sync
cp .env.example .env   # then add your OpenAI key and Logfire write/read tokens
```

## Files

| File | What it does |
| --- | --- |
| `trivia_tools.py` | `TriviaTools` with `get_categories()` and `get_questions(amount, category, difficulty)` (provided) |
| `trivia_agent.py` | The agent, Logfire instrumentation and the `run()` loop; a session is wrapped in `logfire.span('trivia_session')` |
| `query_traces.py` | Lists `trivia_session` trace IDs and how many agent runs each contains |
| `trace_replay/` | From the course lesson, changed to sum tokens over every `invoke_agent` span in a trace and to read `gen_ai.aggregated_usage.*` |
| `session_cost.py` | Rebuilds the grouped session as an `AgentRunResult` and calculates its cost |

```bash
uv run python trivia_agent.py     # play a session
uv run python query_traces.py     # find session trace IDs
uv run python session_cost.py     # replay a session and price it
```

## Answers

| Q | Answer | How |
| --- | --- | --- |
| 1 | `get_categories` | First call in every run: `get_categories({})`, then `get_questions({"amount":3,"category":23,"difficulty":"medium"})` |
| 2 | `invoke_agent agent` | The only span with no parent; it contains the `chat gpt-4o-mini` and `execute_tool ...` spans |
| 3 | 6 | 1 run for the opening prompt + 1 per answer (5); `stop` exits without a run |
| 4 | 2,000 - 10,000 | 5,496 input tokens across the 6 runs - each run resends the whole message history, so input grows every turn |
| 5 | `01a17af2d3b8862693a5c22175a03afa` | The only `trivia_session` trace; it contains 6 `invoke_agent agent` spans |
| 6 | Less than $0.01 | 5,496 input + 843 output tokens = $0.00133 at gpt-4o-mini prices |
| 7 (bonus) | `logfire.attach_context()` | Feedback logged inside the open session span is already in the trace; when it arrives later (e.g. a separate web request), save `logfire.get_context()` and attach it before `logfire.info(...)` |

## Notes

- The course `trace_replay` kept only the latest agent span, which for a grouped session reports only the last run's tokens. I sum over all spans and keep the latest span's messages (they already contain the full conversation).
- In the current PydanticAI the agent span stores totals as `gen_ai.aggregated_usage.input_tokens` / `output_tokens`; reading only `gen_ai.usage.*` returned 0 tokens.
- This `logfire` version requires `min_timestamp` in `query_json_rows()`.
