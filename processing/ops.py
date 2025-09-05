import numpy as np

# Core image ops expect uint8 arrays.
# Channel order for inputs/outputs is RGB (not BGR).

# Import utility functions
from .utils import _ensure_numpy, _pil_to_numpy, _numpy_to_pil


# Import functions from specialized modules to maintain clean separation of concerns
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
