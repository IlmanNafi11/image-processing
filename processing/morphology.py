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

def _preprocess_for_morphology(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = 255 - thresh
    return binary

def erosion_square_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 3)
    result = cv2.erode(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def erosion_square_5(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 5)
    result = cv2.erode(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def erosion_cross_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('cross', 3)
    result = cv2.erode(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def dilation_square_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 3)
    result = cv2.dilate(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def dilation_square_5(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 5)
    result = cv2.dilate(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def dilation_cross_3(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('cross', 3)
    result = cv2.dilate(binary, kernel, iterations=1)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def opening_square_9(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 9)
    result = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def closing_square_9(img: np.ndarray) -> np.ndarray:
    _ensure_numpy()
    binary = _preprocess_for_morphology(img)
    kernel = _get_structuring_element('square', 9)
    result = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    if img.ndim == 3:
        return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result
