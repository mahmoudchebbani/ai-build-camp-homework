from dotenv import load_dotenv

load_dotenv()

from pydantic_ai import Agent  # noqa: E402

from tools import get_page, search_wikipedia

instructions = """
You're a helpful assistant that answers questions using Wikipedia.

Always search Wikipedia first with search_wikipedia to find relevant pages,
then use get_page to read the most relevant ones before answering.
Base your answer on the page content and mention which pages you used.
""".strip()

wikipedia_agent = Agent(
    "openai:gpt-4o-mini",
    instructions=instructions,
    tools=[search_wikipedia, get_page],
)


def tool_calls(result):
    calls = []
    for message in result.all_messages():
        for part in message.parts:
            if part.part_kind == "tool-call":
                calls.append((part.tool_name, part.args))
    return calls


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "Where do capybaras live?"
    result = wikipedia_agent.run_sync(question)
    for name, args in tool_calls(result):
        print(f"TOOL {name}({args})")
    print()
    print(result.output)
    print()
    print(result.usage)
