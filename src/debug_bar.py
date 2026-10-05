import sys
sys.path.append('c:\\NextLeap Projects\\Sri Ganesh\\MVP\\src\\phase1')
from embedding_service import MultimodalEmbeddingModel
from vector_store import VectorDatabase

emb = MultimodalEmbeddingModel()
db = VectorDatabase(persist_directory='c:\\NextLeap Projects\\Sri Ganesh\\MVP\\src\\chroma_db')
query = "interior of a pub or bar with stools, drinks, and liquor bottles"
vec = emb.get_text_embedding(query)
res = db.query_photos("user_123", vec, top_k=10)
print(f"Query: {query}")
for i in range(len(res['ids'][0])):
    print(f"File: {res['metadatas'][0][i]['filename']} | Distance: {res['distances'][0][i]:.2f}")
