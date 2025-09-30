import numpy as np
import cv2
from .utils import _ensure_numpy

def _get_structuring_element(shape: str, size: int) -> np.ndarray:
    if shape == 'square':
        return cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    elif shape == 'cross':
        return cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
    else:
        raise ValueError(f"Unknown shape: {shape}")

def erosion_square_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 3)
    return cv2.erode(img, kernel, iterations=1)

def erosion_square_5(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 5)
    return cv2.erode(img, kernel, iterations=1)

def erosion_cross_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('cross', 3)
    return cv2.erode(img, kernel, iterations=1)

def dilation_square_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 3)
    return cv2.dilate(img, kernel, iterations=1)

def dilation_square_5(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 5)
    return cv2.dilate(img, kernel, iterations=1)

def dilation_cross_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('cross', 3)
    return cv2.dilate(img, kernel, iterations=1)

def opening_square_9(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 9)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing_square_9(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    kernel = _get_structuring_element('square', 9)
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
