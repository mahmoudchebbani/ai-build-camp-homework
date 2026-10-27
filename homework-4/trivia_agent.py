import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent

from trivia_tools import TriviaTools

load_dotenv()

# reads LOGFIRE_TOKEN (the project's write token) from .env
logfire.configure()
logfire.instrument_pydantic_ai()

instructions = """You are a trivia quizmaster. When asked to play trivia:
1. Use the available tools to fetch trivia questions
2. Ask the player one question at a time with multiple choice options
3. Wait for their answer before moving to the next question
4. When the player answers, explain why the correct answer is correct - add interesting context and facts
5. After all questions, give the final score
"""

trivia_tools = TriviaTools()

agent = Agent(
    'openai:gpt-4o-mini',
    name='agent',
    tools=[trivia_tools.get_categories, trivia_tools.get_questions],
    instructions=instructions,
)


def tool_calls(messages):
    calls = []
    for m in messages:
        for p in m.parts:
            if p.part_kind == 'tool-call':
                calls.append((p.tool_name, p.args))
    return calls


def play():
    message_history = []
    user_input = input("You: ")

    while user_input.strip().lower() not in {"quit", "exit", ""}:
        result = agent.run_sync(user_input, message_history=message_history)
        for name, args in tool_calls(result.new_messages()):
            print(f"  [tool call] {name}({args})")
        print(f"\nQuizmaster: {result.output}\n")

        message_history = result.all_messages()
        user_input = input("You: ")


def run(prompt):
    message_history = []

    while True:
        result = agent.run_sync(prompt, message_history=message_history)
        print(result.output)
        message_history = result.all_messages()

        prompt = input("You (write 'stop' to stop): ")
        if not prompt or prompt.lower().strip() == 'stop':
            break


if __name__ == "__main__":
    with logfire.span('trivia_session'):
        run("Let's play 5 easy questions from Science & Nature")
