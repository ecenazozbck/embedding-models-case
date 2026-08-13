import json
import os
import time
import numpy as np
import faiss
import cohere

co = cohere.Client(os.environ["COHERE_API_KEY"])

index = faiss.read_index("data/cohere.index")
with open("data/cohere_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)
with open("data/paraphrase_test_set.json", "r", encoding="utf-8") as f:
    test_set = json.load(f)

paraphrases = [row["paraphrase"] for row in test_set]
expected_sqls = [row["expected_sql"] for row in test_set]

start_time = time.time()
response = co.embed(
    texts=paraphrases,
    model="embed-multilingual-v3.0",
    input_type="search_query"
)
embed_time = time.time() - start_time

query_vectors = np.array(response.embeddings).astype("float32")
faiss.normalize_L2(query_vectors)

correct_at_1 = 0
correct_at_3 = 0
reciprocal_ranks = []

search_start = time.time()
for i, qv in enumerate(query_vectors):
    qv = qv.reshape(1, -1)
    scores, indices = index.search(qv, 3)
    top_3_sqls = [metadata[str(idx)]["sql"] for idx in indices[0]]

    if top_3_sqls[0] == expected_sqls[i]:
        correct_at_1 += 1
    if expected_sqls[i] in top_3_sqls:
        correct_at_3 += 1
        rank = top_3_sqls.index(expected_sqls[i]) + 1
        reciprocal_ranks.append(1 / rank)
    else:
        reciprocal_ranks.append(0)
search_time = time.time() - search_start

mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
avg_query_time_ms = (embed_time + search_time) / len(paraphrases) * 1000

print(f"Recall@1: {correct_at_1}/{len(test_set)} = {correct_at_1/len(test_set):.2%}")
print(f"Recall@3: {correct_at_3}/{len(test_set)} = {correct_at_3/len(test_set):.2%}")
print(f"MRR: {mrr:.4f}")
print(f"Ort. sorgu basina sure: {avg_query_time_ms:.2f} ms")