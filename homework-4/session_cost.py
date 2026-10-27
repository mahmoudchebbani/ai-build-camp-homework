import os

from dotenv import load_dotenv
from logfire.query_client import LogfireQueryClient

from trace_replay import fetch_trace, trace_to_run_result

load_dotenv()

MODEL_PRICES = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def calculate_cost(model_name, input_tokens, output_tokens):
    prices = MODEL_PRICES[model_name.lower()]
    input_cost = (input_tokens / 1_000_000) * prices["input"]
    output_cost = (output_tokens / 1_000_000) * prices["output"]
    return input_cost + output_cost


SESSION_TRACE_ID = "01a17af2d3b8862693a5c22175a03afa"

if __name__ == "__main__":
    client = LogfireQueryClient(read_token=os.environ["LOGFIRE_READ_TOKEN"])

    trace = fetch_trace(SESSION_TRACE_ID, client)
    result = trace_to_run_result(trace)

    usage = result.usage
    cost = calculate_cost("gpt-4o-mini", usage.input_tokens, usage.output_tokens)

    print(f"messages in reconstructed run: {len(result.all_messages())}")
    print(f"final output: {str(result.output)[:120]}...")
    print(f"input tokens: {usage.input_tokens}, output tokens: {usage.output_tokens}")
    print(f"cost: ${cost:.6f}")
