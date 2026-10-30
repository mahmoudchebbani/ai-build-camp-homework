"""Compare the LLM judge's labels with my manual labels ("bad" is the positive class)."""
import json
import sys

judged_file = sys.argv[1] if len(sys.argv) > 1 else "results_judged.json"

with open(judged_file) as f:
    judged = json.load(f)
with open("results_labeled.json") as f:
    human = {r["question"]: r["label"] for r in json.load(f)}

tp = fp = fn = tn = 0
for r in judged:
    j, h = r["judge_label"], human[r["question"]]
    if j == "bad" and h == "bad":
        tp += 1
    elif j == "bad" and h == "good":
        fp += 1
    elif j == "good" and h == "bad":
        fn += 1
    else:
        tn += 1

total = tp + fp + fn + tn
accuracy = (tp + tn) / total
precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0

print(f"{judged_file}: disagreements={fp + fn}")
print(f"TP={tp} FP={fp} FN={fn} TN={tn} (total {total})")
print(f"accuracy  = {accuracy:.3f}")
print(f"precision = {precision:.3f}")
print(f"recall    = {recall:.3f}")

almond = next(r for r in judged if "almond milk" in r["question"])
print(f"\nalmond milk - human: {human[almond['question']]}, judge: {almond['judge_label']}")
print(f"judge reasoning: {almond['judge_reasoning']}")
