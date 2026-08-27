"""
Lightweight Image Quality Screening Module.
Performs resolution, blur (Laplacian variance), and illumination checks prior to inference.
Inspired by Section 15 of prompt & Mahin & Li (2026).
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Any


class ImageQualityChecker:
    """
    Quality control pipeline validating skin lesion images prior to ML inference.
    """

    def __init__(
        self,
        min_resolution: int = 150,
        blur_threshold: float = 60.0,
        min_brightness: float = 30.0,
        max_brightness: float = 230.0
    ):
        self.min_resolution = min_resolution
        self.blur_threshold = blur_threshold
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

    def inspect_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Runs quality checks on a PIL Image instance.
        """
        w, h = image.size
        resolution_ok = (w >= self.min_resolution) and (h >= self.min_resolution)

        # Convert PIL to OpenCV BGR numpy array
        img_np = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # 1. Blur detection using Laplacian variance
        blur_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        blur_ok = blur_var >= self.blur_threshold

        # 2. Illumination / Brightness check
        mean_brightness = float(np.mean(gray))
        brightness_ok = (mean_brightness >= self.min_brightness) and (mean_brightness <= self.max_brightness)

        # Overall quality determination
        is_valid = resolution_ok and blur_ok and brightness_ok

        # Compute normalized quality score (0.0 to 1.0)
        res_score = min(1.0, (w * h) / (224.0 * 224.0))
        blur_score = min(1.0, blur_var / (self.blur_threshold * 2.0))
        bright_score = 1.0 - abs(mean_brightness - 128.0) / 128.0
        
        overall_score = float(np.clip(0.4 * res_score + 0.4 * blur_score + 0.2 * bright_score, 0.1, 1.0))

        details = []
        if not resolution_ok:
            details.append(f"Low resolution: {w}x{h} px (min required: {self.min_resolution}x{self.min_resolution} px).")
        if not blur_ok:
            details.append(f"Image appears blurry or out of focus (Variance: {blur_var:.1f}).")
        if not brightness_ok:
            if mean_brightness < self.min_brightness:
                details.append("Image is too dark / underexposed.")
            else:
                details.append("Image is overexposed / glaring.")

        return {
            'is_valid': is_valid,
            'overall_score': overall_score,
            'resolution': f"{w}x{h}",
            'resolution_ok': resolution_ok,
            'blur_variance': round(blur_var, 2),
            'blur_ok': blur_ok,
            'brightness_mean': round(mean_brightness, 2),
            'brightness_ok': brightness_ok,
            'details': details,
            'message': "Image quality is suitable for analysis." if is_valid else "; ".join(details)
        }


if __name__ == '__main__':
    checker = ImageQualityChecker()
    dummy_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    result = checker.inspect_image(dummy_img)
    print("Quality Result:", result)
