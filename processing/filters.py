import numpy as np
import cv2
from PIL import Image
from .utils import _ensure_numpy

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not available, using fallback implementation")

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
    
    return prewitt(img)

def edge_detection_2(img: np.ndarray) -> np.ndarray:
    
    return sobel(img)

def edge_detection_3(img: np.ndarray) -> np.ndarray:

    _ensure_numpy()
    gray = _to_grayscale_if_needed(img)

    # Canny edge detection with threshold values
    # Lower threshold: 50, Upper threshold: 150
    edges = cv2.Canny(gray, 50, 150)

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

def flip_horizontal(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return cv2.flip(img, 1)

def flip_vertical(img: np.ndarray) -> np.ndarray:
    
    _ensure_numpy()
    return cv2.flip(img, 0)

def rotate(img: np.ndarray, angle: float) -> np.ndarray:
    
    _ensure_numpy()
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    rotated = cv2.warpAffine(img, rotation_matrix, (width, height))
    return rotated

def translate(img: np.ndarray, tx: int, ty: int) -> np.ndarray:
    
    _ensure_numpy()
    height, width = img.shape[:2]
    
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    
    translated = cv2.warpAffine(img, translation_matrix, (width, height))
    return translated

def zoom(img: np.ndarray, scale_factor: float) -> np.ndarray:
    
    _ensure_numpy()
    height, width = img.shape[:2]
    
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    zoomed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    if scale_factor > 1.0:
        x_start = (new_width - width) // 2
        y_start = (new_height - height) // 2
        result = zoomed[y_start:y_start + height, x_start:x_start + width]
    else:
        result = np.zeros((height, width, img.shape[2] if img.ndim == 3 else 1), dtype=img.dtype)
        x_start = (width - new_width) // 2
        y_start = (height - new_height) // 2
        if img.ndim == 3:
            result[y_start:y_start + new_height, x_start:x_start + new_width] = zoomed
        else:
            result[y_start:y_start + new_height, x_start:x_start + new_width, 0] = zoomed
    
    return result

def crop(img: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    
    _ensure_numpy()
    img_height, img_width = img.shape[:2]
    
    x = max(0, min(x, img_width - 1))
    y = max(0, min(y, img_height - 1))
    
    x_end = min(x + width, img_width)
    y_end = min(y + height, img_height)
    
    if x >= x_end or y >= y_end:
        return img.copy()
    
    cropped = img[y:y_end, x:x_end].copy()
    return cropped

def remove_background(img: np.ndarray) -> np.ndarray:

    _ensure_numpy()

    if REMBG_AVAILABLE:
        # Use rembg for AI-based background removal
        try:
            # Convert numpy array to PIL Image
            if img.ndim == 2:
                # Grayscale to RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                pil_img = Image.fromarray(img_rgb)
            else:
                # Assume RGB or BGR
                if img.shape[2] == 3:
                    # Convert BGR to RGB for PIL
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(img_rgb)
                else:
                    # Already has alpha or other format
                    pil_img = Image.fromarray(img)

            # Use rembg to remove background
            result_pil = remove(pil_img)

            # Convert back to numpy array
            result_np = np.array(result_pil)

            # rembg returns RGBA, we need to composite with white background
            if result_np.shape[2] == 4:  # RGBA
                # Split into RGB and alpha
                rgb = result_np[:, :, :3]
                alpha = result_np[:, :, 3:4] / 255.0

                # Create white background
                white_bg = np.ones_like(rgb) * 255

                # Composite: foreground * alpha + background * (1 - alpha)
                result_rgb = (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)

                # Convert back to BGR for OpenCV compatibility
                result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
                return result_bgr
            else:
                # If no alpha channel, assume it's already processed
                return cv2.cvtColor(result_np, cv2.COLOR_RGB2BGR)

        except Exception as e:
            print(f"rembg failed: {e}, falling back to custom implementation")
            # Fall through to custom implementation

    # Fallback: Custom OpenCV-based implementation
    # Ensure image is in RGB format
    if img.ndim == 2:
        # Grayscale to BGR
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 1:
        # Single channel to BGR
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    original_height, original_width = img.shape[:2]

    max_dimension = 500
    if original_width > max_dimension or original_height > max_dimension:
        scale = max_dimension / max(original_width, original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else:
        img_resized = img.copy()
        new_width = original_width
        new_height = original_height

    # Convert to grayscale for processing
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding for better foreground detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding to handle varying lighting conditions
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Also try Otsu thresholding as fallback
    _, otsu_thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Combine adaptive and Otsu results
    combined_mask = cv2.bitwise_or(adaptive_thresh, otsu_thresh)

    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_resized = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_resized = cv2.morphologyEx(mask_resized, cv2.MORPH_OPEN, kernel, iterations=1)

    # If mask is mostly empty, try a different approach
    if np.sum(mask_resized) < (mask_resized.size * 0.1):
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask_resized = np.zeros_like(gray)
        if contours:
            cv2.drawContours(mask_resized, contours, -1, 255, -1)

            kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            mask_resized = cv2.morphologyEx(mask_resized, cv2.MORPH_CLOSE, kernel_large, iterations=3)

    mask_resized = cv2.GaussianBlur(mask_resized, (3, 3), 0)

    if new_width != original_width or new_height != original_height:
        mask_final = cv2.resize(mask_resized, (original_width, original_height), interpolation=cv2.INTER_LINEAR)
        mask_final = cv2.GaussianBlur(mask_final, (3, 3), 0)
        _, mask_final = cv2.threshold(mask_final, 127, 255, cv2.THRESH_BINARY)
    else:
        mask_final = mask_resized

    result = np.ones_like(img) * 255

    mask_3ch = cv2.cvtColor(mask_final, cv2.COLOR_GRAY2BGR) / 255.0
    result = (img * mask_3ch + result * (1 - mask_3ch)).astype(np.uint8)

    return result