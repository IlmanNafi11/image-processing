import numpy as np
from PyQt5.QtGui import QImage, QPixmap


def pixmap_to_numpy(pix: QPixmap) -> np.ndarray:
    """Convert QPixmap to numpy array in RGB format"""
    img = pix.toImage()
    if img.isNull():
        raise ValueError("QImage is null")

    # Ensure ARGB32 backing for predictable byte layout (BGRA in memory)
    img = img.convertToFormat(img.Format_ARGB32)

    w = img.width()
    h = img.height()
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    arr = np.frombuffer(ptr, np.uint8).reshape((h, img.bytesPerLine() // 4, 4))
    # BGRA -> RGB
    rgb = arr[:, :w, 0:3][:, :, ::-1]
    return rgb.copy()


def numpy_to_pixmap(arr: np.ndarray) -> QPixmap:
    """Convert numpy array to QPixmap"""
    if arr.ndim == 2:
        h, w = arr.shape
        # Convert to 3-channel grayscale for display
        arr_rgb = np.stack([arr, arr, arr], axis=2)
    elif arr.ndim == 3 and arr.shape[2] == 3:
        h, w, _ = arr.shape
        arr_rgb = arr
    else:
        raise ValueError("Unsupported array shape for image: %r" % (arr.shape,))

    # Ensure contiguous in memory
    arr_rgb = np.ascontiguousarray(arr_rgb)
    # Create QImage from numpy array
    qimg = QImage(arr_rgb.data, w, h, 3 * w, QImage.Format_RGB888)
    # Deep copy to detach from numpy memory
    return QPixmap.fromImage(qimg.copy())
