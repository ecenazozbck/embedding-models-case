import json
import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load the index + metadata (built from the ORIGINAL/deduped dataset — unchanged)
index = faiss.read_index("data/trmteb.index")
with open("data/trmteb_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load your paraphrase test set
with open("data/paraphrase_test_set.json", "r", encoding="utf-8") as f:
    test_set = json.load(f)

model = SentenceTransformer("selmanbaysan/bert-base-turkish-uncased-cachedmnrl-contrastive-loss")

paraphrases = [row["paraphrase"] for row in test_set]
expected_sqls = [row["expected_sql"] for row in test_set]

print(f"Testing {len(paraphrases)} paraphrases...")

start_time = time.time() #hız ölçümü için
query_vectors = model.encode(paraphrases, batch_size=32).astype("float32")
embed_time = time.time() - start_time 

faiss.normalize_L2(query_vectors)

correct_at_1 = 0
correct_at_3 = 0
reciprocal_ranks = []

search_start = time.time()
for i, qv in enumerate(query_vectors):
    qv = qv.reshape(1, -1)
    scores, indices = index.search(qv, 3) #cosine sim skor
    top_3_sqls = [metadata[str(idx)]["sql"] for idx in indices[0]]

    if top_3_sqls[0] == expected_sqls[i]:
        correct_at_1 += 1
    if expected_sqls[i] in top_3_sqls:
        correct_at_3 += 1

    if expected_sqls[i] in top_3_sqls:
        rank = top_3_sqls.index(expected_sqls[i]) + 1 
        reciprocal_ranks.append(1/rank)
    else:
        reciprocal_ranks.append(0)

search_time = time.time() - search_start

mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
avg_query_time_ms = (embed_time + search_time) / len(paraphrases)*1000

print(f"\nRecall@1: {correct_at_1}/{len(test_set)} = {correct_at_1/len(test_set):.2%}")
print(f"Recall@3: {correct_at_3}/{len(test_set)} = {correct_at_3/len(test_set):.2%}")
print(f"MRR: {mrr:.4f}")
print(f"Ort. sorgu başına süre: {avg_query_time_ms:.2f} ms")