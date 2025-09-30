import numpy as np
import cv2
from .utils import _ensure_numpy

def identity(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return img.copy()

def _to_grayscale_if_needed(img: np.ndarray) -> np.ndarray:
    
    if img.ndim == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def _to_rgb_stack(gray_img: np.ndarray) -> np.ndarray:
    
    return np.stack([gray_img, gray_img, gray_img], axis=2)

def edge_detection_1(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    gray = _to_grayscale_if_needed(img)

    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]], dtype=np.float32)

    edges = cv2.filter2D(gray, -1, kernel)
    return _to_rgb_stack(edges)

def edge_detection_2(img: np.ndarray) -> np.ndarray:
    
    return prewitt(img)

def edge_detection_3(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    gray = _to_grayscale_if_needed(img)

    kernel = np.array([[0,  1, 0],
                       [1, -4, 1],
                       [0,  1, 0]], dtype=np.float32)

    edges = cv2.filter2D(gray, -1, kernel)
    edges = np.abs(edges)
    edges = np.clip(edges * 2, 0, 255).astype(np.uint8)

    return _to_rgb_stack(edges)

def sharpen(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    if img.ndim == 3 and img.shape[2] == 3:
        channels = cv2.split(img)
        sharpened_channels = []
        for ch in channels:
            sharpened = _sharpen_channel(ch)
            sharpened_channels.append(sharpened)
        return cv2.merge(sharpened_channels)
    else:
        return _sharpen_channel(img)

def _sharpen_channel(channel: np.ndarray) -> np.ndarray:
    
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]], dtype=np.float32)

    sharpened = cv2.filter2D(channel, -1, kernel)
    return np.clip(sharpened, 0, 255).astype(np.uint8)

def gaussian_blur_3x3(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return cv2.GaussianBlur(img, (3, 3), 0)

def gaussian_blur_5x5(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return cv2.GaussianBlur(img, (5, 5), 0)

def unsharp_masking(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    mask = cv2.subtract(img, blurred)

    sharpened = cv2.addWeighted(img, 1.5, mask, 0.5, 0)
    return sharpened

def average_filter(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    kernel = np.ones((3, 3), np.float32) / 9
    return cv2.filter2D(img, -1, kernel)

def low_pass_filter(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return cv2.GaussianBlur(img, (5, 5), 1.0)

def high_pass_filter(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    low_pass = cv2.GaussianBlur(img, (5, 5), 1.0)

    high_pass = cv2.subtract(img, low_pass)

    high_pass = cv2.add(high_pass, 128)

    return high_pass

def bandstop_filter(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    blur_small = cv2.GaussianBlur(img, (3, 3), 0.5)
    blur_large = cv2.GaussianBlur(img, (9, 9), 2.0)

    bandstop = cv2.subtract(blur_small, blur_large)

    bandstop = cv2.add(bandstop, 128)

    return bandstop

def prewitt(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    gray = _to_grayscale_if_needed(img)

    kernel_x = np.array([[-1, 0, 1],
                         [-1, 0, 1],
                         [-1, 0, 1]], dtype=np.float32)

    kernel_y = np.array([[-1, -1, -1],
                         [0,  0,  0],
                         [1,  1,  1]], dtype=np.float32)

    edges_x = cv2.filter2D(gray, -1, kernel_x)
    edges_y = cv2.filter2D(gray, -1, kernel_y)
    edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)

    return _to_rgb_stack(edges)

def sobel(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    gray = _to_grayscale_if_needed(img)

    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]], dtype=np.float32)

    kernel_y = np.array([[-1, -2, -1],
                         [0,  0,  0],
                         [1,  2,  1]], dtype=np.float32)

    edges_x = cv2.filter2D(gray, -1, kernel_x)
    edges_y = cv2.filter2D(gray, -1, kernel_y)
    edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)

    return _to_rgb_stack(edges)