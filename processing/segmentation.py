import numpy as np
import cv2
from .utils import _ensure_numpy, _pil_to_numpy, _numpy_to_pil

def global_thresholding(img: np.ndarray, threshold: int = 127) -> np.ndarray:

    _ensure_numpy()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    if img.ndim == 3:
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    return thresh

def adaptive_thresholding(img: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:

    _ensure_numpy()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

    if img.ndim == 3:
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    return thresh

def kmeans_segmentation(img: np.ndarray, k: int = 3) -> np.ndarray:

    _ensure_numpy()
    if img.ndim == 3:
        pixel_values = img.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
    else:
        pixel_values = img.reshape((-1, 1))
        pixel_values = np.float32(pixel_values)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]

    if img.ndim == 3:
        segmented_image = segmented_data.reshape(img.shape)
    else:
        segmented_image = segmented_data.reshape(img.shape)

    return segmented_image

def watershed_segmentation(img: np.ndarray) -> np.ndarray:

    _ensure_numpy()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)

    markers = markers + 1
    markers[unknown == 255] = 0

    if img.ndim == 3:
        markers = cv2.watershed(img, markers)
    else:
        markers = cv2.watershed(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB), markers)

    if img.ndim == 3:
        img[markers == -1] = [255, 0, 0]
    else:
        img[markers == -1] = 255

    return img

def region_growing_segmentation(img: np.ndarray, seed_point: tuple = None, threshold: int = 10) -> np.ndarray:

    _ensure_numpy()
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img.copy()

    if seed_point is None:
        seed_point = (gray.shape[1] // 2, gray.shape[0] // 2)

    h, w = gray.shape
    segmented = np.zeros((h, w), np.uint8)
    visited = np.zeros((h, w), np.uint8)

    seed_value = gray[seed_point[1], seed_point[0]]
    stack = [seed_point]

    while stack:
        x, y = stack.pop()
        if visited[y, x] == 1:
            continue
        visited[y, x] = 1

        if abs(int(gray[y, x]) - int(seed_value)) <= threshold:
            segmented[y, x] = 255

            if x > 0 and visited[y, x-1] == 0:
                stack.append((x-1, y))
            if x < w-1 and visited[y, x+1] == 0:
                stack.append((x+1, y))
            if y > 0 and visited[y-1, x] == 0:
                stack.append((x, y-1))
            if y < h-1 and visited[y+1, x] == 0:
                stack.append((x, y+1))

    if img.ndim == 3:
        return cv2.cvtColor(segmented, cv2.COLOR_GRAY2RGB)
    return segmented