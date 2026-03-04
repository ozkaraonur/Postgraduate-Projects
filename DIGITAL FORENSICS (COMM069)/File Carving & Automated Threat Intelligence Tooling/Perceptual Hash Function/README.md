# Image Similarity Toolkit 📸

A lightweight Python utility for building an image fingerprint database and identifying visually similar images using **Perceptual Hashing (pHash)**.

Unlike cryptographic hashes (MD5, SHA-1) which change entirely if a single pixel is modified, these scripts use `aHash` and `dHash` to identify images that have been resized, compressed, or slightly edited.

## Features
- **Visual Fingerprinting:** Uses `Average Hashing` and `Difference Hashing`.
- **Similarity Scoring:** Detects matches based on Hamming Distance.
- **Persistent Storage:** Saves image fingerprints to a portable JSON database.
- **Efficient Scanning:** Recursively walks through directories to catalog images.

## Prerequisites

Ensure you have Python 3.x installed, then install the required dependencies:

```bash
pip install ImageHash Pillow
```

## How to Use

### 1. Build the Fingerprint Database
Scan a directory of images to generate their visual hashes and save them to a JSON file. This "fingerprints" your library for future comparisons.

```bash
python build_db.py <image_directory> <output_db.json>
```
### 2. Check for Matches
Compare a specific image against your existing database to find duplicates or near-matches.

```bash
python check_image.py <target_image> <db_file.json>
```
### How it Works
The scripts utilize Hamming Distance to compare hashes. Instead of comparing pixels directly, it compares the binary "fingerprints" of the images.

| Distance | Interpretation |
| :--- | :--- |
| **0** | **Exact Match:** The images are visually identical. |
| **1–5** | **High Similarity:** Likely a resized version or a different compression level. |
| **5–10** | **Potentially Related:** Could be a cropped version or a similar composition. |
| **>10** | **Different:** The images are likely unrelated. |
