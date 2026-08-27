"""
ABCDE Rule Clinical Feature Extractor.
Extracts quantitative Asymmetry (A), Border Irregularity (B), Color Variation (C),
Estimated Diameter (D), and Evolution (E) scores directly from lesion images and clinical context.
Grounded in clinical dermatology guidelines & HAM10000 metadata.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any


class ABCDEExtractor:
    """
    Extracts ABCDE dermatological parameters using computer vision and clinical metadata.
    """

    @staticmethod
    def extract_abcde_scores(image_pil: Image.Image, evolution_str: str = "static") -> Dict[str, Any]:
        """
        Calculates ABCDE feature scores for skin lesion image.
        """
        img_np = np.array(image_pil.convert('RGB'))
        h, w, _ = img_np.shape

        # 1. Grayscale & Otsu Thresholding to isolate lesion mask
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)

            # Asymmetry (A): Compare top/bottom and left/right mask overlap
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            else:
                cx, cy = w // 2, h // 2

            # Left/Right symmetry comparison
            left_half = thresh[:, :cx]
            right_half = cv2.flip(thresh[:, cx:2*cx], 1) if 2*cx <= w else cv2.flip(thresh[:, cx:], 1)
            min_w = min(left_half.shape[1], right_half.shape[1])
            diff_lr = np.sum(np.abs(left_half[:, :min_w].astype(float) - right_half[:, :min_w].astype(float)))
            asymmetry_score = float(np.clip((diff_lr / (area + 1e-5)) * 5.0, 1.2, 9.8))

            # Border Irregularity (B): Compactness ratio (Perimeter^2 / (4 * pi * Area))
            if area > 0:
                compactness = (perimeter ** 2) / (4 * np.pi * area)
                border_score = float(np.clip(compactness * 2.5, 1.5, 9.5))
            else:
                border_score = 4.0
        else:
            asymmetry_score = 3.5
            border_score = 3.0
            area = 500.0

        # Color Variation (C): Standard deviation across R, G, B channels
        stds = [np.std(img_np[:, :, c]) for c in range(3)]
        color_std_mean = float(np.mean(stds))
        color_score = float(np.clip((color_std_mean / 40.0) * 10.0, 1.0, 9.9))

        # Diameter Estimation (D): Estimated max diameter in mm (assuming 224px ~ 15mm field of view)
        estimated_diameter_mm = float(np.clip(np.sqrt(area) * (15.0 / 224.0), 2.0, 18.0))

        # Evolution (E): Score based on reported recent changes
        if evolution_str == 'changed_recently':
            evolution_score = 9.0
            evolution_text = "High Evolution (Recent enlargement/darkening reported)"
        elif evolution_str == 'uncertain':
            evolution_score = 5.0
            evolution_text = "Moderate Evolution (Uncertain history)"
        else:
            evolution_score = 2.0
            evolution_text = "Static (No recent changes reported)"

        return {
            'asymmetry_score': round(asymmetry_score, 1),
            'border_score': round(border_score, 1),
            'color_score': round(color_score, 1),
            'diameter_mm': round(estimated_diameter_mm, 1),
            'evolution_score': round(evolution_score, 1),
            'evolution_text': evolution_text,
            'summary': f"A: {asymmetry_score:.1f}/10, B: {border_score:.1f}/10, C: {color_score:.1f}/10, D: {estimated_diameter_mm:.1f}mm, E: {evolution_score:.1f}/10"
        }


if __name__ == '__main__':
    dummy_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    abcde = ABCDEExtractor.extract_abcde_scores(dummy_img, 'changed_recently')
    print("ABCDE Scores:", abcde)
