from model2vec import StaticModel

model = StaticModel.from_pretrained("atasoglu/1mb-turkish-embeddings")
embedding = model.encode(["Bu ay ne kadar ciro yaptım?"])
print(len(embedding[0]))