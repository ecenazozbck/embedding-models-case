import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

index = faiss.read_index("data/e5_large.index")
with open("data/e5_large_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer("intfloat/multilingual-e5-large")

test_question = "Bu ayki satışlarım ne kadar?"

query_vector = model.encode([test_question]).astype("float32")

k = 3
distances, indices = index.search(query_vector, k)

print(f"Query: {test_question}\n")
for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
    match = metadata[str(idx)]
    print(f"#{rank} (distance={dist:.4f})")
    print(f"Matched question: {match['question']}")
    print(f"SQL: {match['sql']}")
    print()

