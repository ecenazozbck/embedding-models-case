import json
with open("data/golden_queries_.json", "r", encoding="utf-8") as f:
    data =json.load(f)

for i, item in enumerate(data):
    item["id"] = i

print(f"Before: {len(data)} recs")

seen_questions = set()
deduped = []

for item in data:
    q = item["question"]
    if q not in seen_questions:
        seen_questions.add(q)
        deduped.append(item)

print(f"After: {len(deduped)}")
print(f"Removed: {len(data) - len(deduped)}")

with open("data/golden_queries_deduped.json", "w", encoding="utf-8") as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)

