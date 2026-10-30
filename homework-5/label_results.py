"""Manual labels for results.json -> labels.csv (and results_labeled.json).

Labels were decided by reading every response against recipes.json.
"""
import csv
import json

# question number (1-based, order of scenarios.csv) -> (label, failure_category, note)
LABELS = {
    1: ("good", "", "matches recipe 6; adds a small 'prevent scrambling' tip (borderline)"),
    2: ("good", "", "Thai Green Curry, ingredients and times match recipe 7"),
    3: ("good", "", "stir fry, miso soup, Greek salad - all tagged healthy, details match"),
    4: ("bad", "hallucination", "no sushi recipe, then gives a full general sushi recipe"),
    5: ("good", "", "425F, 12-14 min - matches recipe 9"),
    6: ("good", "", "carbonara, times match; could also mention other pasta (none exist)"),
    7: ("good", "", "all 3 Italian recipes, details match"),
    8: ("good", "", "steps, temps and times match recipe 14"),
    9: ("good", "", "35 min cook + 10 prep - matches recipe 13"),
    10: ("good", "", "serves 4 - matches recipe 7"),
    11: ("bad", "invented-substitution", "says bacon works; recipe says nothing about substitutes"),
    12: ("bad", "invented-substitution", "says almond milk works; no tool call, recipe only lists milk"),
    13: ("bad", "not-grounded", "right conclusion (anchovies) but from general knowledge; invents rennet point and offers a vegetarian Caesar recipe it doesn't have"),
    14: ("good", "", "stir fry + falafel tagged vegan, miso shown with its vegan-adaptable tag"),
    15: ("good", "", "correctly says no gluten-free recipes are tagged"),
    16: ("good", "", "says calories aren't in the recipe (offer to calculate is borderline)"),
    17: ("good", "", "says it has no ramen recipe"),
    18: ("good", "", "says it has no beef bourguignon"),
    19: ("good", "", "declines restaurant question"),
    20: ("bad", "out-of-scope-answered", "gives dishwasher troubleshooting instead of declining"),
    21: ("bad", "contradicts-recipe", "says canned chickpeas are fine; recipe says do not use canned"),
    22: ("good", "", "says don't boil - matches recipe 10; extra reasoning is general knowledge (borderline)"),
    23: ("bad", "hallucination", "invents fridge/freezer storage times"),
    24: ("bad", "hallucination", "invents wine pairings"),
}

with open("results.json") as f:
    results = json.load(f)

assert len(results) == len(LABELS)

for i, row in enumerate(results, 1):
    row["label"], row["failure_category"], row["note"] = LABELS[i]

with open("results_labeled.json", "w") as f:
    json.dump(results, f, indent=2)

with open("labels.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["question", "category", "type", "label", "failure_category", "note"])
    for row in results:
        w.writerow([row["question"], row["category"], row["type"], row["label"], row["failure_category"], row["note"]])

bad = [r for r in results if r["label"] == "bad"]
print(f"bad: {len(bad)} / {len(results)}")
print(f"bad in the first 20: {sum(r['label'] == 'bad' for r in results[:20])} / 20")
for r in bad:
    print(f"  {r['failure_category']:22} {r['question']}")
