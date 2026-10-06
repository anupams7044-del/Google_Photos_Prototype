import json
with open('c:/NextLeap Projects/Sri Ganesh/MVP/src/phase1/offline_vectors.json', 'r') as f:
    v = json.load(f)

code = 'VECTORS = ' + repr(v) + '''

def populate_db_if_empty(db_path="chroma_db"):
    import chromadb
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("photos")
    if collection.count() == 0:
        print("Auto-populating database...")
        ids = list(VECTORS.keys())
        embeddings = list(VECTORS.values())
        metadatas = [{"filename": k} for k in ids]
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
        print("Done!")
'''

with open('c:/NextLeap Projects/Sri Ganesh/MVP/src/auto_populate.py', 'w') as f:
    f.write(code)
