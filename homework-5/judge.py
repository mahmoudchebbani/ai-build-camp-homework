import json
import sys

from pydantic import BaseModel
from typing import Literal
from pydantic_ai import Agent


class JudgeEvaluation(BaseModel):
    reasoning: str
    label: Literal["good", "bad"]


with open('recipes.json') as f:
    RECIPES = json.load(f)

RECIPE_DATA = json.dumps(RECIPES, indent=1)

judge_instructions = f"""You are an expert evaluator assessing a recipe assistant that answers
cooking questions using a fixed recipe collection. The full collection is given
below in <RECIPES>. Use it to check every factual claim in the response.

A response is "good" if:
1. It accurately answers using ONLY information from the recipe collection
2. It correctly identifies when a recipe is not available and says so
3. It correctly identifies out-of-scope questions (not about cooking/recipes) and declines

A response is "bad" if ANY of these apply:
1. It makes up recipes, ingredients, or instructions not in the collection (hallucination)
2. It provides cooking advice (substitutions, nutrition info, storage tips, pairings) that it
   invented rather than found in the recipe data
3. It answers a question it should have declined (not about recipes, or recipe not available),
   including giving general how-to steps after saying it doesn't have the recipe
4. It gives incorrect information from the recipes (wrong times, wrong ingredients, wrong steps)
5. It says it cannot help when a matching recipe exists in the collection

How to judge:
- Check claims against <RECIPES>. If a claim matches the recipe data (ingredients,
  steps, times, temperatures, servings, tags, or warnings written in the instructions),
  it is grounded - even if it is detailed or reworded. Do not mark a response bad just
  because it is detailed.
- Simple derivations from the data are fine: adding prep and cook time, listing recipes
  that share a tag, or reformatting steps.
- Judge what the response claims, not what it offers. Offering to search, to show more
  details, or to help with something else is not hallucination. It only counts if the
  response actually states invented facts.
- Small explanations that only restate a rule from the recipe (e.g. why a step is done)
  are acceptable; new facts that the recipe doesn't contain (new temperatures, times,
  substitutes, storage, nutrition, safety claims) are not.
- When the data can't answer the question, the right answer says so. Saying "the
  recipe doesn't specify" is good; filling the gap with general knowledge is bad.

<RECIPES>
{RECIPE_DATA}
</RECIPES>
"""


judge_agent = Agent(
    'openai:gpt-4o-mini',
    output_type=JudgeEvaluation,
    instructions=judge_instructions,
)

results_file = sys.argv[1] if len(sys.argv) > 1 else 'results.json'
judged_file = sys.argv[2] if len(sys.argv) > 2 else 'results_judged.json'

with open(results_file) as f:
    results = json.load(f)

for i, row in enumerate(results):
    prompt = f"""Question: {row['question']}
Agent response: {row['output']}"""

    evaluation = judge_agent.run_sync(prompt)
    row['judge_label'] = evaluation.output.label
    row['judge_reasoning'] = evaluation.output.reasoning
    print(f"[{i+1}/{len(results)}] {row['judge_label']}: {row['question']}")

with open(judged_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved judged results to {judged_file}")
