import os
from PIL import Image
import shutil

RAW_DIR = "raw_photos"
OUT_DIR = r"phase1\sample_photos"

def prep_photos():
    # 1. Create the directories if they don't exist
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    photos_to_process = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic', '.webp', '.jfif'))]
    
    if len(photos_to_process) == 0:
        print(f"⚠️ No photos found in the '{RAW_DIR}' folder.")
        print(f"Please copy your 500 original photos into the 'src/{RAW_DIR}' folder and run this script again.")
        return

    print(f"Found {len(photos_to_process)} photos. Emptying old database photos...")
    
    # 2. Clear out the old dummy photos
    for file in os.listdir(OUT_DIR):
        file_path = os.path.join(OUT_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # 3. Compress and resize the new photos
    print(f"Compressing photos and saving to {OUT_DIR} (This may take a minute)...")
    processed_count = 0
    
    for filename in photos_to_process:
        try:
            filepath = os.path.join(RAW_DIR, filename)
            with Image.open(filepath) as img:
                # Convert to standard RGB (removes transparent backgrounds if PNG)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Shrink the image so the longest side is 500px (keeps file size tiny for GitHub)
                img.thumbnail((500, 500))
                
                # Save as a highly compressed JPEG
                out_path = os.path.join(OUT_DIR, f"memory_{processed_count}.jpg")
                img.save(out_path, "JPEG", optimize=True, quality=75)
                processed_count += 1
                
        except Exception as e:
            print(f"Could not process {filename}: {e}")

    print("--------------------------------------------------")
    print(f"Success! {processed_count} photos have been compressed and staged.")
    print("Your photos are now small enough to host for free on the cloud!")
    print("Next step: Run `python phase1/ingestion_pipeline.py` in your terminal to build the AI database.")

if __name__ == "__main__":
    prep_photos()
