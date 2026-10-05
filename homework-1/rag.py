import json

from dotenv import load_dotenv
from openai import OpenAI

from index_books import build_index

index, _ = build_index()
load_dotenv()
openai_client = OpenAI()

instructions = """
You're a course assistant, your task is to answer the QUESTION from the
course students using the provided CONTEXT
"""

prompt_template = """
<QUESTION>
{question}
</QUESTION>

<CONTEXT>
{context}
</CONTEXT>
""".strip()


def build_prompt(question, search_results):
    context = json.dumps(search_results, indent=2)
    prompt = prompt_template.format(
        question=question,
        context=context
    ).strip()
    return prompt


def search(question):
    return index.search(question, num_results=5)


def llm(user_prompt, instructions, model='gpt-4o-mini'):
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = openai_client.responses.create(
        model=model,
        input=messages
    )

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    return response.output_text, usage


def rag(query):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, usage = llm(prompt, instructions)
    return answer, usage


if __name__ == "__main__":
    answer, usage = rag("python function definition")
    print(answer)
    print(usage)
