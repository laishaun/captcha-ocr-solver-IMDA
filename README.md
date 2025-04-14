# Captcha OCR Solver (Strategy 2: Preprocessing + OCR)

This project implements a simple OCR pipeline to recognize 5-character captchas. It uses contrast enhancement to preprocess images and EasyOCR to extract the characters. This was coded using python 3.13.3

---

## 🧠 Strategy Overview

- Each captcha contains **exactly 5 characters**: uppercase letters (A–Z) and digits (0–9).
- Font, spacing, and background are consistent across samples.
- Strategy 2 focuses on **contrast enhancement** followed by **end-to-end OCR** using [EasyOCR](https://github.com/JaidedAI/EasyOCR).

---

## 📁 Project Structure

```
captcha-ocr-solver/
├── captcha/
│   └── solver.py           # Contains the Captcha class
├── test_images/            # Drop your input captcha images here
├── outputs/                # Output .txt files will be saved here
├── run.py                  # Script to run OCR on a folder of images
├── requirements.txt        # List of required Python packages
├── .gitignore              # Standard Git ignore rules
└── README.md               # This file
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/laishaun/captcha-ocr-solver-IMDA.git
cd captcha-ocr-solver-IMDA
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Place your test captcha images in the `images_to_test/` folder. Supported formats: `.jpg`, `.jpeg`, `.png`.

2. Run the OCR script:

```bash
python run.py --input images_to_test/ --output outputs/
```

3. Each result will be saved as a `.txt` file inside the `outputs/` folder, using the same base filename.

You will also see prediction results printed to the console like:

```
input00.jpg | PRED: EGYK4
input01.jpg | PRED: 8Z7AG
```

---

## 📸 Screenshots

### Example Captcha Image

![Sample Captcha](https://raw.githubusercontent.com/laishaun/captcha-ocr-solver-IMDA/main/test_images/input00.jpg)

### Output Example

```
outputs/input00.txt → EGYK4
```

---

## 🔍 How It Works

The core logic is in `captcha/solver.py`. For each image:

1. Apply contrast enhancement using OpenCV.
2. Convert to RGB.
3. Use EasyOCR to predict characters.
4. Save the output to a `.txt` file.

The `Captcha` class follows the provided template:

```python
class Captcha:
    def __init__(self):
        ...

    def __call__(self, im_path, save_path):
        ...
```

---

## 🙋‍♂️ Notes

- This is a proof-of-concept using basic image enhancement and OCR.
- Future improvements could include character-level segmentation or a CNN+CTC model.

---

## 🧠 Author

Shaun Lai  
[https://github.com/laishaun](https://github.com/laishaun)
