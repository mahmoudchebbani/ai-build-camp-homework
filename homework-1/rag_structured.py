from typing import Literal

from pydantic import BaseModel, Field

from rag import build_prompt, instructions, openai_client, search


class RAGResponse(BaseModel):
    answer: str = Field(description="The main answer to the user's question in markdown")
    found_answer: bool = Field(description="True if relevant information was found in the documentation")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    confidence_explanation: str = Field(description="Explanation about the confidence level")
    answer_type: Literal["how-to", "explanation", "troubleshooting", "comparison", "reference"] = Field(description="The category of the answer")
    followup_questions: list[str] = Field(description="Suggested follow-up questions")


def llm_structured(user_prompt, instructions, output_type=RAGResponse, model='gpt-4o-mini'):
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]

    response = openai_client.responses.parse(
        model=model,
        input=messages,
        text_format=output_type
    )

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    return response.output_parsed, usage


def rag_structured(query):
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, usage = llm_structured(prompt, instructions)
    return answer, usage


if __name__ == "__main__":
    answer, usage = rag_structured("python function definition")
    print(answer.model_dump_json(indent=2))
    print(usage)
