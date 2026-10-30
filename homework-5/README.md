# Homework 5: Evaluating a Recipe Assistant

Starter code from the course gist. Two fixes to it: `recipe_agent.py` loads `.env`, and `run_scenarios.py` reads `result.usage` as a property (PydanticAI 2.x).

## Setup

```bash
cp .env.example .env   # add OPENAI_API_KEY
uv sync
uv run python run_scenarios.py                 # scenarios.csv -> results.json
uv run python label_results.py                 # manual labels -> labels.csv
uv run --env-file .env python judge.py         # results.json -> results_judged.json
uv run python alignment.py                     # judge vs manual labels
```

`run_scenarios.py` and `judge.py` take optional input/output file arguments, so the synthetic run doesn't overwrite the hand-crafted one.

## Answers

**Q1. Almond milk in pancakes.** The agent hallucinates. It made no tool calls in any of 3 runs and gave general substitution advice that isn't from the recipe collection.

**Q2. Cost of one run.** Less than $0.001 (almond milk: 230 input + 79 output tokens = $0.000082).

**Q3. Manual labels.** 8 bad out of 24 scenarios (5 bad in the first 20). The failures were sushi, bacon, almond milk, Caesar (not grounded), dishwasher, canned falafel, storage and wine.

**Q4. Original judge.** 16 bad out of 24. The judge never sees the recipe data, so it can't tell grounded answers from made-up ones.

**Q5. Almond milk, judge vs me.** Both of us said bad. TP 8, FP 8, FN 0, TN 8. Accuracy 0.667, precision 0.50, recall 1.00.

**Q6. Improved judge** (`judge.py`; the original is `judge_v1.py`). It gets the recipe data plus general rules: claims that match the data are grounded, simple derivations are fine, judge claims rather than offers, and "the recipe doesn't specify" is a good answer. Disagreements went from 8 to 2. Accuracy 0.917, precision 0.80, recall 1.00. The two left (gluten-free, ramen) are borderline "offers alternatives" answers.

**Q7. Synthetic dataset (bonus).** `generate_synthetic.py` makes 5 questions per recipe (75 in total). The improved judge marked **62/75 = 82.7% bad**, compared with about 42% (10/24) on the hand-crafted set.

| category | bad |
|---|---|
| factual | 7/15 |
| how-to | 13/15 |
| detail | 12/15 |
| substitution | 15/15 |
| comparison | 15/15 |

Same root cause as the hand-crafted set: the agent made **0 tool calls on all 75 questions** and answered from general knowledge. Synthetic questions show it more clearly, because they ask about the recipes in the collection. Every "why", "how do I" and "compare with" question gets a confident general cooking answer instead of the collection's recipe.

New patterns the hand-crafted set didn't show:

- Comparisons with dishes outside the collection (pepperoni pizza, butter chicken) always fail.
- "This recipe" questions have no context, so the agent asks which recipe is meant or guesses.

Not covered by the synthetic set: out-of-scope and adversarial questions (sushi, dishwasher, wine) only come from writing scenarios by hand.
