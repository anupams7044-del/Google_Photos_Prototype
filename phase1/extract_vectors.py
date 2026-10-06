import json
from vector_store import VectorDatabase

db = VectorDatabase(persist_directory="c:/NextLeap Projects/Sri Ganesh/MVP/src/phase1/chroma_db")
collection = db._get_user_collection("user_123")
results = collection.get(include=["embeddings", "metadatas"])

offline_map = {}
for idx, meta in enumerate(results['metadatas']):
    filename = meta['filename']
    emb = results['embeddings'][idx]
    offline_map[filename] = emb

with open("c:/NextLeap Projects/Sri Ganesh/MVP/src/offline_vectors.json", "w") as f:
    json.dump(offline_map, f)
print("Saved offline vectors.")
