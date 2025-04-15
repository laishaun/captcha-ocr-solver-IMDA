# Captcha OCR Solver (Main Strategy: Preprocessing + OCR)

This project implements a simple OCR pipeline to recognize 5-character captchas. It uses contrast enhancement to preprocess images and EasyOCR to extract the characters. This was coded using python 3.13.3

---

## SolverMain Function Overview

- Each captcha contains **exactly 5 characters**: uppercase letters (A–Z) and digits (0–9).
- Font, spacing, and background are consistent across samples.
- Strategy 2 focuses on **contrast enhancement** followed by **end-to-end OCR** using [EasyOCR](https://github.com/JaidedAI/EasyOCR).

---
## SolverExperiment Function Overview
Given the consistent visual characteristics of the CAPTCHA images — fixed background texture, uniform spacing, and a controlled character set — I hypothesized that a background subtraction method may isolate foreground text more effectively than general-purpose OCR alone. An alternate pipeline was developed to explore this idea.

- Explore a low-compute, interpretable approach that leverages the high similarity between samples
- Evaluate whether subtracting a statistical background model would improve text clarity for OCR systems
- Compare the output quality to the baseline model (SolverMain.py) which uses brightness and contrast enhancement alone

To achieve this, an alternate pipeline (SolverExperiment.py) was developed that:
- Builds a statistical background model using a median composite of training images (sample_captchas/)
- Subtracts the background from unseen CAPTCHA images (images_to_test/)
- Applies normalization and OCR using EasyOCR
- Saves prediction results to the same output/ directory, for side-by-side comparison

This experiment was deliberately kept modular to avoid interference with the main solver and to allow for independent evaluation.

## Project Structure

```
captcha-ocr-solver/
├── captcha_solver/
│   └── SolverMain.py           # Contains the main captcha solver class
│   └── SolverExperiment.py     # Contains the secondary experiment using background subtraction
├── images_to_test/             # Drop your input captcha images here
├── output/                     # Output .txt files will be saved here
├── run.py                      # Script to run OCR on a folder of images
├── sample_captchas             # Sample images provided in the original challenge (also used as base set for background model)
├── requirements.txt            # List of required Python packages
├── .gitignore                  # Standard Git ignore rules
└── README.md                   # This file
```

---

## Installation

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

Note:  > This project was built with Python 3.13.3 and may not work properly with older versions.

## Usage

1. Place your test captcha images in the `images_to_test/` folder. Supported formats: `.jpg`, `.jpeg`, `.png`. (Samples are available in the sample_captchas folder for your convenience to drag and drop, please do not remove, they are also used for the background model build)

2. Run the OCR script:

```bash
python run.py

```

3. Each result will be saved as a `.txt` file inside the `output/` folder, using the same base filename.

You will also see prediction results printed to the console like:

```
input00.jpg | PRED: EGYK4
input01.jpg | PRED: 8Z7AG
```

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
## Strategy and Thought Process
### Problem Framing

The objective is to build a system capable of accurately interpreting 5-character CAPTCHA images for a web form. These CAPTCHA images follow a tightly controlled structure:
- Each CAPTCHA consists of exactly 5 characters.
- The allowable characters are limited to uppercase alphabets (A–Z) and digits (0–9).
- Visual consistency is high across samples: fixed font, consistent kerning, no skew or rotation.
- Backgrounds are uniform and lighter than the characters.
- Images are greyscale or near-greyscale, with minimal variation.

From a trust and governance standpoint:
- The generation process is synthetic and simple, making this a closed-domain problem with likely low entropy.
- Given the limited sample set (25 images), each character appears at least once, allowing for representative sampling but not statistical generalisation. Sample is too small to train CNN with any significant expectation of accuracy
- Future generalisation must consider potential drift in background noise or character rendering.
- This framing assumes that the long-term goal is not just functional performance, but also robustness, interpretability, and auditability—especially relevant for AI deployed in production or regulated environments.


### Solution Formulation

A staged approach was taken to assess both feasibility and longer-term viability. Early efforts focused on establishing baseline performance using pre-trained OCR models with image preprocessing. This allowed me to identify architectural weaknesses and transition toward more robust strategies.


### Strategies Hypothesized

***Strategy 1***: Background Removal with Character Segmentation
- Segment each character based on projection/contour.
- Use classical image processing to remove the consistent background.
- Train a lightweight CNN to classify each of the 5 characters individually.

***Advantages:***
- Transparent and auditable pipeline
- Interpretable outputs with localized errors

***Limitations:***
- Sensitive to minor shifts in alignment or spacing
- Pipeline complexity increases with variability
- Computationally heavy
This method is more aligned with deployment environments requiring high explainability and deterministic behavior.

***Strategy 2***: OCR Baseline with Preprocessing
- Based on initial observations, captchas provided were easily manipulated through manipulation of contrast and brightness
- Use of pre-trained OCR models would be fast and simple solution 

***Advantages:***
- More robust to spacing, noise, or minor distortions
- Scales better to more complex captchas

***Limitations:***
- Reduced interpretability as the OCR model is a black-box process
- Requires significant computational investment and data augmentation

This approach is more suitable for long-term robustness but introduces governance concerns around transparency, model validation, and debugging.

***Conclusion***: Strategy 2 was the primary approach adopted in the initial experiments due to 
- Ability to perform rapid prototyping with COTS models
- Small sample size available
- Ability to quickly iterate


### Initial Experiments: OCR Baseline with Preprocessing

Initial experiments tested OCR libraries (EasyOCR and Tesseract) in conjunction with various preprocessing techniques aimed at improving text visibility and suppressing the uniform background.

Preprocessing methods evaluated:
- Grayscale conversion
- Contrast and brightness adjustment
- image upscaling
- image cropping
- Background subtraction
- Binarization
- Segmentation (character isolation)
- Cropping and upscaling

***Results***:
- Best initial results: 13/24 correct predictions using EasyOCR with grayscale and brightness/contrast tuning.
- Best tied results: 13/24 correct predictions using EasyOCR with background subtraction and grayscale tuning. 
- Worst results: 5/24 correct predictions, segmentation together with background subtraction with Tesseract introduced artifacts that reduced accuracy.
- Tesseract generally underperformed due to its reliance on semantic and contextual information (absent in captchas).
- This phase demonstrated the limitations of using pre-trained, black-box models in a constrained but unfamiliar visual domain.
- Post-processing was discarded as erroneous predictions were not systematic in nature, and were unlikely to improve prediction results 

## Notes

- This is a proof-of-concept using basic image enhancement and OCR.
- Future improvements could include brightness/contrast tuning and background subtraction as complementary preprocessing steps that can be layered with a domain-specific CNN if sufficient samples could be procured. Alternatively, based on the simplistic nature of the captcha generation, synthetic samples would likely be easy to generate as well. 

---

## Author

Shaun Lai  
[https://github.com/laishaun](https://github.com/laishaun)
