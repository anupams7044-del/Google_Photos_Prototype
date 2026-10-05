import sys
import os
print("Starting app_server.py...")
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

# Add phase3 to path to import the stateful backend logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'phase3')))
from advanced_orchestrator import StatefulSearchOrchestrator

app = FastAPI(title="Google Photos AI Discovery MVP")

# Ensure the sample_photos directory exists where images are stored
os.makedirs("phase1/sample_photos", exist_ok=True)

# Mount the static files for the UI and the Images
app.mount("/ui", StaticFiles(directory="phase4"), name="ui")
app.mount("/photos", StaticFiles(directory="phase1/sample_photos"), name="photos")

print("Initializing ML Models and Vector DB... This may take a moment.")
orchestrator = StatefulSearchOrchestrator(db_path="chroma_db")

# Define Data Models for the API
class SearchRequest(BaseModel):
    user_id: str
    query: str

class PivotRequest(BaseModel):
    user_id: str
    session_id: str
    rejected_embeddings: List[List[float]]

@app.get("/")
def read_root():
    """Serves the main HTML UI file."""
    return FileResponse("phase4/index.html")

@app.post("/api/search")
def search(req: SearchRequest):
    """Endpoint to initiate a new search."""
    response = orchestrator.initial_search(req.user_id, req.query)
    if not response:
        raise HTTPException(status_code=404, detail="No results found")
    return response

@app.post("/api/pivot")
def pivot(req: PivotRequest):
    """Endpoint to trigger the 'None of these' dynamic pivot."""
    response = orchestrator.pivot_search(req.user_id, req.session_id, req.rejected_embeddings)
    if not response:
        raise HTTPException(status_code=400, detail="Pivot failed or expired")
    return response

if __name__ == "__main__":
    import uvicorn
    # Support HF Spaces Port
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    
    print("\n--- Starting MVP Web Server ---")
    print(f"Open your browser to: http://localhost:{port}")
    uvicorn.run("app_server:app", host=host, port=port, reload=False)
