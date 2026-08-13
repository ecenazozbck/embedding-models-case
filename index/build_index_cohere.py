import json
import os
import numpy as np
import faiss
import cohere

co = cohere.Client(os.environ["COHERE_API_KEY"])

with open("data/golden_queries_deduped.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i, item in enumerate(data):
    item["id"] = i

questions = [item["question"] for item in data]

print("Embedding via Cohere API...")
embeddings = []
batch_size = 96

for i in range(0, len(questions), batch_size):
    batch = questions[i:i+batch_size]
    response = co.embed(
        texts=batch,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    embeddings.extend(response.embeddings)
    print(f"{i+len(batch)}/{len(questions)}")

embeddings = np.array(embeddings).astype("float32")
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

metadata_dict = {str(item["id"]): item for item in data}
faiss.write_index(index, "data/cohere.index")
with open("data/cohere_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata_dict, f, ensure_ascii=False, indent=2)

print("Bitti.")