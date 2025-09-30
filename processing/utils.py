import numpy as np
from PIL import Image
from typing import Union, Tuple

def _ensure_numpy():
    if np is None:
        raise ImportError("NumPy is required for image processing operations. Please install 'numpy'.")

def _pil_to_numpy(pil_img: Image.Image) -> np.ndarray:
    
    return np.array(pil_img)

def _numpy_to_pil(arr: np.ndarray) -> Image.Image:
    
    if arr.ndim == 2:
        return Image.fromarray(arr, mode='L')
    elif arr.ndim == 3 and arr.shape[2] == 3:
        return Image.fromarray(arr, mode='RGB')
    else:
        raise ValueError(f"Unsupported array shape: {arr.shape}")

def _apply_color_tint(img: np.ndarray, r_factor: float = 1.0, g_factor: float = 1.0,
                     b_factor: float = 1.0, bias: int = 0) -> np.ndarray:
    
    _ensure_numpy()

    img_f = img.astype(np.float32)

    factors = np.array([r_factor, g_factor, b_factor])
    tinted = img_f * factors

    if bias != 0:
        tinted += bias

    return np.clip(tinted, 0, 255).astype(np.uint8)