import sys
import os

# Add phase1 to path to reuse the foundational services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase1')))

from embedding_service import MultimodalEmbeddingModel
from vector_store import VectorDatabase
from clustering_engine import VisualClusteringEngine

class VisualSearchOrchestrator:
    def __init__(self, db_path="../phase1/chroma_db"):
        print("Initializing Search Orchestrator...")
        self.embedding_service = MultimodalEmbeddingModel()
        self.vector_db = VectorDatabase(persist_directory=db_path)
        self.clustering_engine = VisualClusteringEngine(k_clusters=4)

    def search(self, user_id: str, text_query: str, top_k: int = 60):
        """
        Executes the Phase 2 search flow:
        Text Query -> Embedding -> ANN Retrieval -> K-Means Clustering -> Centroid Selection
        """
        print(f"\nUser '{user_id}' searching for: '{text_query}'")
        
        # 1. Generate text embedding
        query_vector = self.embedding_service.get_text_embedding(text_query)
        
        # 2. ANN Candidate Pool Retrieval
        print(f"Retrieving top {top_k} candidate images...")
        results = self.vector_db.query_photos(user_id, query_vector, top_k=top_k)
        
        ids = results.get('ids', [[]])[0]
        embeddings = results.get('embeddings', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not ids or not embeddings:
             print("No results found in Vector DB. Please run the ingestion pipeline in Phase 1 first.")
             return None
             
        print(f"Found {len(ids)} candidates. Segmenting into 4 distinct visual themes...")
        
        # 3 & 4. Real-Time Clustering & Centroid Selection
        centroids = self.clustering_engine.cluster_and_get_centroids(embeddings, metadatas, ids)
        
        print("\n=== 2x2 Visual Choice Grid Results ===")
        for idx, c in enumerate(centroids):
            print(f"Quadrant {idx+1}:")
            print(f"  Photo ID: {c['photo_id']}")
            print(f"  Source Image: {c['metadata'].get('filename', 'Unknown')}")
            print(f"  (Represents Conceptual Cluster {c['cluster_id']})")
        print("======================================\n")
            
        return centroids

if __name__ == "__main__":
    # Test execution
    orchestrator = VisualSearchOrchestrator()
    
    # Simulating a vague memory search
    test_query = "a relaxing beach trip"
    orchestrator.search(user_id="user_123", text_query=test_query)
