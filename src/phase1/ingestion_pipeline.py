import os
import uuid
from embedding_service import MultimodalEmbeddingModel
from vector_store import VectorDatabase

class PhotoIngestionPipeline:
    def __init__(self, db_path="./chroma_db"):
        print("Initializing Embedding Model (This may take a moment to download weights)...")
        self.embedding_service = MultimodalEmbeddingModel()
        print("Initializing Vector Database...")
        self.vector_db = VectorDatabase(persist_directory=db_path)

    def process_upload(self, user_id: str, photo_path: str, metadata: dict = None):
        """Simulates the background asynchronous task of processing an uploaded photo."""
        print(f"Processing upload for {photo_path}...")
        
        # 1. Generate Multimodal Embedding
        embedding = self.embedding_service.get_image_embedding(photo_path)
        if embedding is None:
            return False

        # 2. Extract/Merge Metadata (simulating EXIF extraction)
        photo_id = str(uuid.uuid4())
        final_metadata = {
            "source_path": photo_path,
            "filename": os.path.basename(photo_path),
            "upload_timestamp": "2026-10-03T10:00:00Z" # Dummy timestamp for MVP
        }
        if metadata:
            final_metadata.update(metadata)

        # 3. Index securely in Vector DB
        self.vector_db.insert_photo(user_id, photo_id, embedding, final_metadata)
        return True

    def batch_process_directory(self, user_id: str, directory_path: str):
        """Helper function to ingest an entire folder of images for MVP testing."""
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} not found. Creating it now.")
            os.makedirs(directory_path, exist_ok=True)
            print(f"Please place some test images (.jpg, .png) inside {directory_path} and run again.")
            return

        supported_formats = ('.png', '.jpg', '.jpeg', '.webp')
        files_found = False
        
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(supported_formats):
                files_found = True
                file_path = os.path.join(directory_path, filename)
                self.process_upload(user_id, file_path)
                
        if not files_found:
             print(f"No supported images found in {directory_path}. Add some to test the pipeline.")

if __name__ == "__main__":
    # Test execution
    pipeline = PhotoIngestionPipeline()
    
    test_dir = "phase1/sample_photos"
    print(f"\n--- Starting Batch Ingestion for MVP Test ---")
    pipeline.batch_process_directory(user_id="user_123", directory_path=test_dir)
