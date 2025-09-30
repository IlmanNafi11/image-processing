import numpy as np
from typing import Tuple
from .utils import _ensure_numpy

def bit_depth(img: np.ndarray, bits: int) -> np.ndarray:
    
    _ensure_numpy()
    bits = int(bits)
    bits = max(1, min(8, bits))

    levels = 2 ** bits
    step = 256 // levels

    quant_map = np.zeros(256, dtype=np.uint8)
    for i in range(levels):
        start = i * step
        end = min((i + 1) * step, 256)
        mid = (start + end) // 2
        quant_map[start:end] = mid

    quantized = quant_map[img]

    return quantized

