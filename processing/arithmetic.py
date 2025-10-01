import numpy as np
from .utils import _ensure_numpy

def _apply_binary_operation(img1: np.ndarray, img2: np.ndarray, operation) -> np.ndarray:
    _ensure_numpy()
    img1, img2 = ensure_same_dimensions(img1, img2)
    result = operation(img1.astype(np.float32), img2.astype(np.float32))
    return np.clip(result, 0, 255).astype(np.uint8)

def _apply_constant_operation(img: np.ndarray, constant: float, operation) -> np.ndarray:
    _ensure_numpy()
    result = operation(img.astype(np.float32), constant)
    return np.clip(result, 0, 255).astype(np.uint8)

def add_images(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    return _apply_binary_operation(img1, img2, lambda a, b: a + b)

def add_constant(img: np.ndarray, constant: float) -> np.ndarray:
    return _apply_constant_operation(img, constant, lambda a, c: a + c)

def subtract_images(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    return _apply_binary_operation(img1, img2, lambda a, b: a - b)

def subtract_constant(img: np.ndarray, constant: float) -> np.ndarray:
    return _apply_constant_operation(img, constant, lambda a, c: a - c)


def multiply_images(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    return _apply_binary_operation(img1, img2, lambda a, b: a * b / 255.0)

def multiply_constant(img: np.ndarray, constant: float) -> np.ndarray:
    return _apply_constant_operation(img, constant, lambda a, c: a * c)

def divide_images(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    def divide_operation(a, b):
        b_copy = b.copy()
        b_copy[b_copy == 0] = 1
        return a / b_copy * 255.0
    return _apply_binary_operation(img1, img2, divide_operation)

def divide_constant(img: np.ndarray, constant: float) -> np.ndarray:
    if constant == 0:
        raise ValueError("Cannot divide by zero")
    return _apply_constant_operation(img, constant, lambda a, c: a / c)


def resize_image_to_match(img: np.ndarray, target_shape: tuple) -> np.ndarray:
    
    _ensure_numpy()
    import cv2
    target_height, target_width = target_shape[:2]
    resized = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    return resized

def ensure_same_dimensions(img1: np.ndarray, img2: np.ndarray) -> tuple:
    
    if img1.shape == img2.shape:
        return img1, img2

    resized_img2 = resize_image_to_match(img2, img1.shape)
    return img1, resized_img2