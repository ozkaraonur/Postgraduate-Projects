import sys
import json
import imagehash
from PIL import Image

# Threshold for similarity (Hamming distance)
# 0-5 is usually considered similar for PHFs.
SIMILARITY_THRESHOLD = 5

def get_hashes(image_path):
    try:
        img = Image.open(image_path)
        a_hash = imagehash.average_hash(img)
        d_hash = imagehash.dhash(img)
        return a_hash, d_hash
    except Exception as e:
        print(f"Error opening target image: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python check_image.py <target_image> <db_file.json>")
        sys.exit(1)

    target_image_path = sys.argv[1]
    db_path = sys.argv[2]

    print(f"[*] Analyzing target image: {target_image_path}")
    
    # load database
    try:
        with open(db_path, 'r') as f:
            database = json.load(f)
    except FileNotFoundError:
        print("Database file not found.")
        sys.exit(1)

    # Compute hashes for the suspect image
    target_a, target_d = get_hashes(target_image_path)
    
    print(f"    Target aHash: {target_a}")
    print(f"    Target dHash: {target_d}")
    print("-" * 50)

    matches_found = False

    for filename, data in database.items():
        # Convert stored strings back to ImageHash objects
        db_a = imagehash.hex_to_hash(data['a_hash'])
        db_d = imagehash.hex_to_hash(data['d_hash'])

        # Calculate Hamming Distance
        dist_a = target_a - db_a
        dist_d = target_d - db_d

        # Check if either hash is within the threshold
        if dist_a <= SIMILARITY_THRESHOLD or dist_d <= SIMILARITY_THRESHOLD:
            matches_found = True
            print(f"[!] MATCH FOUND: {filename}")
            print(f"    Similarity: aHash Dist={dist_a}, dHash Dist={dist_d}")
            
            if dist_a == 0 and dist_d == 0:
                print("    -> Exact Match")
            else:
                print("    -> Visual Similarity Detected")
            print("-" * 20)

    if not matches_found:
        print("[OK] No similar images found in the database.")

if __name__ == "__main__":
    main()
