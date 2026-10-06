import requests
import json

API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/clip-ViT-B-32"
headers = {"Authorization": "Bearer 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"}

def query(texts):
    response = requests.post(API_URL, headers=headers, json={"inputs": texts})
    return response.json()

output = query(["a photo of a cat"])
print("Type:", type(output))
if isinstance(output, list) and len(output) > 0:
    print("Vector length:", len(output[0]))
    print("First 5 values:", output[0][:5])
else:
    print("Error:", output)
