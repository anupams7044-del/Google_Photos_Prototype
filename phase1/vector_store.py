import chromadb
from chromadb.config import Settings

class VectorDatabase:
    def __init__(self, persist_directory="./chroma_db"):
        # Initialize ChromaDB persistent client for local MVP storage
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def _get_user_collection(self, user_id: str):
        # Multi-tenant partitioning: Each user gets their own secure collection
        collection_name = f"user_{user_id}"
        return self.client.get_or_create_collection(name=collection_name)

    def insert_photo(self, user_id: str, photo_id: str, embedding: list, metadata: dict):
        """Inserts a single photo's vector and metadata into the user's secure partition."""
        collection = self._get_user_collection(user_id)
        collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[photo_id]
        )
        print(f"Inserted photo {photo_id} into Vector DB for user {user_id}")

    def query_photos(self, user_id: str, query_embedding: list, top_k: int = 100):
        """Performs Approximate Nearest Neighbor (ANN) search for a given user."""
        collection = self._get_user_collection(user_id)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["embeddings", "metadatas", "distances"]
        )
        return results
