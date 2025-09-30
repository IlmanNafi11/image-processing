import numpy as np
import cv2
from .utils import _ensure_numpy

def histogram_equalization(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    if img.ndim == 2:
        return cv2.equalizeHist(img)
    elif img.ndim == 3 and img.shape[2] == 3:
        channels = cv2.split(img)
        eq_channels = [cv2.equalizeHist(ch) for ch in channels]
        return cv2.merge(eq_channels)
    else:
        raise ValueError(f"Unsupported image shape: {img.shape}")

def fuzzy_histogram_equalization_rgb(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Fuzzy HE RGB requires RGB image")

    img_f = img.astype(np.float32)

    result_channels = []
    for ch in range(3):
        channel = img_f[:, :, ch]
        eq_channel = _fuzzy_equalize_channel(channel)
        result_channels.append(eq_channel)

    result = cv2.merge(result_channels)
    return np.clip(result, 0, 255).astype(np.uint8)

def fuzzy_histogram_equalization_grayscale(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    if img.ndim == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif img.ndim == 2:
        gray = img
    else:
        raise ValueError(f"Unsupported image shape: {img.shape}")

    eq_gray = _fuzzy_equalize_channel(gray.astype(np.float32))

    eq_rgb = np.stack([eq_gray, eq_gray, eq_gray], axis=2)
    return np.clip(eq_rgb, 0, 255).astype(np.uint8)

def _fuzzy_equalize_channel(channel: np.ndarray) -> np.ndarray:
    

    dark_center = 64
    medium_center = 128
    bright_center = 192
    width = 64

    dark_membership = _triangular_membership(channel, dark_center, width)
    medium_membership = _triangular_membership(channel, medium_center, width)
    bright_membership = _triangular_membership(channel, bright_center, width)

    hist_dark = cv2.calcHist([channel.astype(np.uint8)], [0], None, [256], [0, 256])
    hist_medium = cv2.calcHist([channel.astype(np.uint8)], [0], None, [256], [0, 256])
    hist_bright = cv2.calcHist([channel.astype(np.uint8)], [0], None, [256], [0, 256])

    eq_hist_dark = cv2.equalizeHist(channel.astype(np.uint8))
    eq_hist_medium = cv2.equalizeHist(channel.astype(np.uint8))
    eq_hist_bright = cv2.equalizeHist(channel.astype(np.uint8))

    result = (dark_membership * eq_hist_dark +
              medium_membership * eq_hist_medium +
              bright_membership * eq_hist_bright) / (dark_membership + medium_membership + bright_membership + 1e-6)

    return result

def _triangular_membership(x: np.ndarray, center: float, width: float) -> np.ndarray:
    
    left = center - width
    right = center + width

    membership = np.zeros_like(x, dtype=np.float32)
    mask_left = (x >= left) & (x < center)
    mask_right = (x >= center) & (x <= right)

    membership[mask_left] = (x[mask_left] - left) / (center - left)
    membership[mask_right] = (right - x[mask_right]) / (right - center)

    return membership