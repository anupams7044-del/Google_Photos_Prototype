import os
import requests
import time

class MultimodalEmbeddingModel:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
        self.headers = {"Authorization": "Bearer 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"}
        
    def get_image_embedding(self, image_path):
        """Offline MVP: We do not process new images dynamically on the server."""
        print("Image processing disabled on the lightweight API tier.")
        return []

    def get_text_embedding(self, text):
        """Extracts a dense vector embedding from a text query via HF API."""
        print(f"Calling HuggingFace API for: '{text}'...")
        for _ in range(5):  # Retry logic in case the model is waking up
            response = requests.post(self.api_url, headers=self.headers, json={"inputs": text})
            if response.status_code == 200:
                result = response.json()
                # Ensure it is a 1D list of floats
                if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                    return result[0]
                return result
            elif response.status_code == 503:
                print("HF Model is loading, waiting 3 seconds...")
                time.sleep(3)
            else:
                print(f"HF API Error: {response.text}")
                return []
        return []

