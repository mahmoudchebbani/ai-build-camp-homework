import csv
import json

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()


class Question(BaseModel):
    question: str
    category: str
    type: str


class GeneratedQuestions(BaseModel):
    questions: list[Question]


generator = Agent('openai:gpt-4o-mini', output_type=GeneratedQuestions)

with open('recipes.json') as f:
    recipes = json.load(f)

rows = []
for recipe in recipes:
    generation_prompt = f"""Given this recipe, generate 5 questions a user might ask.
Include: 1 factual, 1 how-to, 1 detail, 1 substitution, 1 comparison with another dish.
Use the type as the category (factual, how-to, detail, substitution, comparison).

Recipe: {recipe['name']}
Cuisine: {recipe['cuisine']}
Ingredients: {', '.join(recipe['ingredients'])}
Instructions: {recipe['instructions']}"""

    result = generator.run_sync(generation_prompt)
    for q in result.output.questions:
        rows.append({'question': q.question, 'category': q.category, 'type': recipe['name']})
    print(f"{recipe['name']}: {len(result.output.questions)} questions")

with open('synthetic_scenarios.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['question', 'category', 'type'])
    w.writeheader()
    w.writerows(rows)

print(f"Saved {len(rows)} questions to synthetic_scenarios.csv")
