import json
import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

with open("data/golden_queries_deduped.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#id ekleme
for i, item in enumerate(data):
    item["id"] = i

print(f"{len(data)} adet kayıt.")
print("Örnek soru:", data[0])

questions = [item["question"] for item in data]

model = SentenceTransformer("emrecan/bert-base-turkish-cased-mean-nli-stsb-tr")
print("Embedding...")
embeddings = model.encode(questions, batch_size=32, show_progress_bar=True)

#cosine hazırlığı
embeddings = np.array(embeddings).astype("float32")
faiss.normalize_L2(embeddings)

#build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

metadata_dict = {str(item["id"]): item for item in data}

faiss.write_index(index, "data/emrecan.index")
with open("data/emrecan_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata_dict, f, ensure_ascii=False, indent=2)

print("Bitti. Index ve metadata, id ile kaydedildi.")

