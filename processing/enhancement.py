import numpy as np
from typing import Tuple
from .utils import _ensure_numpy

def invert(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return 255 - img

def log_brightness(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    img_f = img.astype(np.float32)
    img_n = img_f / 255.0
    log_img = np.log1p(img_n)
    log_img /= log_img.max() if log_img.max() > 0 else 1.0
    out = (log_img * 255.0)
    return np.clip(out, 0, 255).astype(np.uint8)

def gamma_correction(img: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    
    _ensure_numpy()
    gamma = max(1e-6, float(gamma))

    if abs(gamma - 1.0) < 1e-6:
        return img.copy()

    inv_gamma = 1.0 / gamma
    lut = np.power(np.arange(256) / 255.0, inv_gamma) * 255.0
    lut = np.clip(lut, 0, 255).astype(np.uint8)

    return lut[img]

def brightness_contrast(img: np.ndarray, brightness: float = 0.0, contrast: float = 1.0) -> np.ndarray:
    
    _ensure_numpy()

    img_f = img.astype(np.float32)

    if brightness != 0:
        img_f += brightness

    if contrast != 1.0:
        img_f = (img_f - 128.0) * contrast + 128.0

    return np.clip(img_f, 0, 255).astype(np.uint8)

