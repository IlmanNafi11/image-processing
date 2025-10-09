import numpy as np

from .utils import _ensure_numpy, _pil_to_numpy, _numpy_to_pil

from .colors import (
    to_grayscale_average,
    to_grayscale_lightness,
    to_grayscale_luminance,
    rgb_yellow,
    rgb_cyan,
    rgb_orange,
    rgb_purple,
    rgb_grey,
    rgb_brown,
    rgb_red
)
from .enhancement import (
    invert,
    log_brightness,
    gamma_correction,
    brightness_contrast
)
from .bitdepth import bit_depth
from .histogram import (
    histogram_equalization,
    fuzzy_histogram_equalization_rgb,
    fuzzy_histogram_equalization_grayscale
)
from .filters import (
    identity,
    canny,
    sharpen,
    gaussian_blur_3x3,
    gaussian_blur_5x5,
    unsharp_masking,
    average_filter,
    low_pass_filter,
    high_pass_filter,
    bandstop_filter,
    prewitt,
    sobel,
    flip_horizontal,
    flip_vertical,
    rotate,
    translate,
    zoom,
    crop,
    remove_background
)
from .arithmetic import (
    add_images,
    add_constant,
    subtract_images,
    subtract_constant,
    multiply_images,
    multiply_constant,
    divide_images,
    divide_constant,
    bitwise_and_images,
    bitwise_or_images,
    bitwise_xor_images
)
from .morphology import (
    erosion_square_3,
    erosion_square_5,
    erosion_cross_3,
    dilation_square_3,
    dilation_square_5,
    dilation_cross_3,
    opening_square_9,
    closing_square_9
)
from .segmentation import (
    global_thresholding,
    adaptive_thresholding,
    kmeans_segmentation,
    watershed_segmentation,
    region_growing_segmentation
)
