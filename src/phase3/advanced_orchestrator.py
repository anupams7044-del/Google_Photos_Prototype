import sys
import os
import uuid

# Add previous phases to path to reuse foundational services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase1')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase2')))

from embedding_service import MultimodalEmbeddingModel
from vector_store import VectorDatabase
from clustering_engine import VisualClusteringEngine
from query_analyzer import QueryAnalyzer
from feedback_processor import FeedbackProcessor

class SearchSession:
    """Manages the state for a single user's search journey."""
    def __init__(self, query_text, initial_vector, enhanced_query=None):
        self.session_id = str(uuid.uuid4())
        self.query_text = query_text
        self.enhanced_query = enhanced_query if enhanced_query else query_text
        self.current_query_vector = initial_vector
        self.pivot_count = 0
        self.max_pivots = 3 # Edge Case Mitigation: Prevents the "Infinite Pivot Trap"

class StatefulSearchOrchestrator:
    def __init__(self, db_path="../phase1/chroma_db"):
        print("Initializing Stateful Search Orchestrator...")
        self.embedding_service = MultimodalEmbeddingModel()
        self.vector_db = VectorDatabase(persist_directory=db_path)
        self.clustering_engine = VisualClusteringEngine(k_clusters=4)
        self.query_analyzer = QueryAnalyzer()
        self.feedback_processor = FeedbackProcessor(negative_weight_factor=0.3)
        
        # In-memory store for active search sessions
        self.active_sessions = {}

    def initial_search(self, user_id: str, text_query: str):
        """Entry point for a new search query."""
        intent = self.query_analyzer.analyze_intent(text_query)
        print(f"\n[Session Start] User '{user_id}' searched: '{text_query}' (Intent Classifier: {intent.upper()})")
        
        if intent == 'specific':
            print("Routing to Legacy Keyword Search (Skipping AI 2x2 Grid).")
            return {"type": "legacy_list", "results": "mock_legacy_results"}
            
        # Prompt Engineering: Taxonomy Mapping for 1-word queries
        lower_q = text_query.lower().strip()
        enhanced_query = text_query
        
        if "bar" in lower_q:
            enhanced_query = "interior of a pub or bar with stools, drinks, and liquor bottles"
        elif "car" in lower_q:
            enhanced_query = "a motor vehicle automobile sports car driving or parked"
        elif "cafe" in lower_q or "coffee" in lower_q:
            enhanced_query = "a coffee shop or cafe interior"
        elif "beach" in lower_q:
            enhanced_query = "a sunny beautiful sandy beach with ocean water"
        elif "party" in lower_q or "birthday" in lower_q:
            enhanced_query = "a kids birthday party celebration with balloons and cake"
            
        initial_vector = self.embedding_service.get_text_embedding(enhanced_query)
        session = SearchSession(text_query, initial_vector, enhanced_query)
        self.active_sessions[session.session_id] = session
        
        return self._execute_visual_retrieval(user_id, session)

    def pivot_search(self, user_id: str, session_id: str, rejected_embeddings: list):
        """Handles the 'None of these' action by applying negative feedback."""
        print(f"\n[Dynamic Pivot] User '{user_id}' clicked 'None of these (Show others)'.")
        
        if session_id not in self.active_sessions:
            print("Error: Session expired or invalid.")
            return None
            
        session = self.active_sessions[session_id]
        
        if session.pivot_count >= session.max_pivots:
            print("Pivot limit reached. Gracefully degrading to fallback search.")
            return {"type": "fallback_message", "message": "We couldn't find exactly what you're looking for. Try a different word."}
            
        session.pivot_count += 1
        print(f"Applying negative vector weights (Pivot {session.pivot_count}/{session.max_pivots})...")
        
        # Recalculate query vector mathematically pushing away from rejected image clusters
        session.current_query_vector = self.feedback_processor.apply_negative_feedback(
            session.current_query_vector, 
            rejected_embeddings
        )
        
        return self._execute_visual_retrieval(user_id, session)

    def _execute_visual_retrieval(self, user_id: str, session: SearchSession):
        """Core logic to fetch and cluster candidates using the session's current vector state."""
        
        # Retrieve candidates based on the mathematically adjusted vector.
        # Fetching exactly top_k=4 so that the 2x2 grid strictly displays the
        # absolute closest semantic matches, bypassing K-Means visual diversity logic
        # which was accidentally surfacing distinct, lower-relevancy items.
        results = self.vector_db.query_photos(user_id, session.current_query_vector, top_k=4)
        
        ids = results.get('ids', [[]])[0]
        embeddings = results.get('embeddings', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]
        
        if not ids:
             return {"type": "error", "message": "No photos found."}
             
        # Strict Relevancy Filter (PM Request: Better to be blank than wrong)
        # If an image's vector distance is absolute garbage, drop it.
        filtered_grid_data = []
        best_distance = distances[0]
        # Relative 15% tolerance threshold
        max_allowed_distance = best_distance * 1.15
        # Absolute garbage threshold: For CLIP L2, anything > 151 is usually totally unrelated.
        ABSOLUTE_CUTOFF = 151.0
        
        print(f"\n=== 2x2 Visual Choice Grid (Session: {session.session_id}) ===")
        
        debug_log = {
            "query": session.enhanced_query,
            "threshold": ABSOLUTE_CUTOFF,
            "results": []
        }
        
        for i in range(len(ids)):
            status = "ACCEPTED"
            if distances[i] > max_allowed_distance or distances[i] >= ABSOLUTE_CUTOFF:
                status = "REJECTED"
                
            debug_log["results"].append({
                "filename": metadatas[i].get('filename', 'Unknown'),
                "distance": float(distances[i]),
                "status": status
            })
            
            if status == "ACCEPTED":
                filtered_grid_data.append({
                    "photo_id": ids[i],
                    "embedding": [float(x) for x in embeddings[i]],
                    "metadata": metadatas[i]
                })
                print(f"Quadrant {len(filtered_grid_data)}: Photo ID {ids[i]} | Source: {metadatas[i].get('filename', 'Unknown')} (Dist: {distances[i]:.2f})")
            else:
                print(f"DROPPED: Source: {metadatas[i].get('filename', 'Unknown')} (Dist: {distances[i]:.2f})")
                
        print("========================================================================\n")
            
        return {
            "type": "2x2_grid", 
            "session_id": session.session_id, 
            "grid_data": filtered_grid_data,
            "debug_log": debug_log
        }

if __name__ == "__main__":
    # Test execution workflow
    orchestrator = StatefulSearchOrchestrator()
    
    # 1. Test routing a specific query (Should bypass AI)
    orchestrator.initial_search("user_123", "IMG_4921.jpg")
    
    # 2. Test initial vague search (Should trigger 2x2 grid)
    response = orchestrator.initial_search("user_123", "a cozy winter dinner")
    
    if response and response['type'] == '2x2_grid':
        session_id = response['session_id']
        grid_data = response['grid_data']
        
        # Simulate user clicking "None of these"
        # We extract the embeddings of the 4 shown quadrants to feed into the negative weight processor
        rejected_vectors = [c['embedding'] for c in grid_data]
        
        # 3. Test Dynamic Pivot (Should apply negative weights and return 4 NEW images)
        pivot_response = orchestrator.pivot_search("user_123", session_id, rejected_vectors)
