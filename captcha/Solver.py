import os
import cv2
import easyocr

class Captcha:
    def __init__(self, alpha=2.5, beta=0):
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.alpha = alpha
        self.beta = beta

    def enhance_contrast(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"❌ Failed to load image: {img_path}")
        enhanced = cv2.convertScaleAbs(img, alpha=self.alpha, beta=self.beta)
        return cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)

    def __call__(self, im_path, save_path):
        image = self.enhance_contrast(im_path)
        results = self.reader.readtext(image, detail=0)
        predicted = ''.join(results).strip().replace(" ", "").replace("\n", "")
        with open(save_path, 'w') as f:
            f.write(predicted)
        print(f"[INFO] {os.path.basename(im_path)} → {predicted}")
        return predicted
