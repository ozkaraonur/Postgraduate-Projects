import os
import sys
import json
import imagehash
from PIL import Image

def generate_hashes(image_path):
    """Generates aHash and dHash for a given image."""
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        
        # Calculate Average Hash (aHash)
        a_hash = imagehash.average_hash(img)
        
        # Calculate Difference Hash (dHash)
        d_hash = imagehash.dhash(img)
        
        return str(a_hash), str(d_hash)
    except Exception as e:
        print(f"[!] Error processing {image_path}: {e}")
        return None, None

def main():
    if len(sys.argv) < 3:
        print("Usage: python build_db.py <image_directory> <output_db_file.json>")
        sys.exit(1)

    image_dir = sys.argv[1]
    output_db = sys.argv[2]
    
    database = {}

    print(f"[*] Scanning directory: {image_dir}...")

    # Iterate over files in the directory
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                full_path = os.path.join(root, file)
                print(f"    Processing: {file}")
                
                a_hash, d_hash = generate_hashes(full_path)
                
                if a_hash and d_hash:
                    # Store in dictionary
                    database[file] = {
                        "path": full_path,
                        "a_hash": a_hash,
                        "d_hash": d_hash
                    }

    # Save to JSON
    with open(output_db, 'w') as f:
        json.dump(database, f, indent=4)

    print(f"\n[+] Database built successfully! Saved {len(database)} entries to {output_db}")

if __name__ == "__main__":
    main()
