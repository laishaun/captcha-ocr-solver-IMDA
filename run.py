import argparse
import os
from captcha_solver.SolverMain import Captcha

def run_batch(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    solver = Captcha()
    for fname in os.listdir(input_dir):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            im_path = os.path.join(input_dir, fname)
            save_path = os.path.join(output_dir, f"{os.path.splitext(fname)[0]}.txt")
            solver(im_path, save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Captcha OCR")
    parser.add_argument("--input", default="images_to_test", help="Folder containing captcha images")
    parser.add_argument("--output", default="output", help="Folder to store prediction text files")
    args = parser.parse_args()
    
    run_batch(args.input, args.output)