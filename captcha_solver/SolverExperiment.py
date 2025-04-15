"""
Alternative solution utilising Background Subtraction for CAPTCHA Recognition

This module builds a background model using provided CAPTCHA images,
subtracts the background, enhances contrast, and applies EasyOCR
to extract text from images.
"""

import os
import cv2
import numpy as np
import easyocr

# === CONFIGURATION ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAMPLE_FOLDER = os.path.join(BASE_DIR, '..', 'sample_captchas')
TEST_FOLDER = os.path.join(BASE_DIR, '..', 'images_to_test')
OUTPUT_FOLDER = os.path.join(BASE_DIR, '..', 'output')

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === BACKGROUND MODELING ===
def build_background_model(image_paths, threshold=80):
    grayscale_images = []
    masks = []

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = gray > threshold

        grayscale_images.append(gray)
        masks.append(mask)

    if not grayscale_images:
        raise ValueError("No valid images found for background modeling.")

    stack = np.stack(grayscale_images)
    mask_stack = np.stack(masks)

    H, W = stack.shape[1:]
    background = np.zeros((H, W), dtype=np.uint8)

    for i in range(H):
        for j in range(W):
            pixels = stack[:, i, j]
            valid = pixels[mask_stack[:, i, j]]
            background[i, j] = np.median(valid) if len(valid) else 255
    return background

# === BACKGROUND SUBTRACTION ===
def subtract_background(image_path, background):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray, background)
    norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
    return norm

# === MAIN PIPELINE ===
def run_experiment_on_first_image():
    sample_images = [os.path.join(SAMPLE_FOLDER, f) for f in os.listdir(SAMPLE_FOLDER) if f.lower().endswith(('.jpg', '.png'))]
    test_images = [f for f in os.listdir(TEST_FOLDER) if f.lower().endswith(('.jpg', '.png'))]

    if not sample_images:
        print("No sample CAPTCHA images found in 'sample_captchas'.")
        return

    if not test_images:
        print("No test CAPTCHA images found in 'images_to_test'.")
        return

    # Use first test image for now
    test_image_path = os.path.join(TEST_FOLDER, test_images[0])
    result_file_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(test_images[0])[0]}_exp.txt")

    background = build_background_model(sample_images, threshold=80)
    cleaned = subtract_background(test_image_path, background)

    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(cleaned, detail=0, paragraph=False)
    predicted = ''.join(result).strip() if result else "No text detected"

    with open(result_file_path, "w") as f:
        f.write(predicted)

    print(f"✅ Processed {os.path.basename(test_image_path)} → {predicted}")

# === EXECUTION ===
if __name__ == "__main__":
    run_experiment_on_first_image()