from typing import Dict, Callable, Optional, Any, TYPE_CHECKING
from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog
from PyQt5.QtCore import QObject
from processing import ops
from .base_classes import BaseManager, ImageOperationResult

if TYPE_CHECKING:
    from .image_processor import ImageProcessor

class ActionManager(BaseManager):
    
    
    def __init__(self, main_window: QMainWindow, image_processor: 'ImageProcessor'):
        super().__init__(main_window)
        self._main_window = main_window
        self._image_processor = image_processor
        self._setup_action_mappings()
    
    def _setup_action_mappings(self) -> None:
        
        
        self._color_actions = {
            'actionYellow': ops.rgb_yellow,
            'actionOrange': ops.rgb_orange,
            'actionCyan': ops.rgb_cyan,
            'actionPurple': ops.rgb_purple,
            'actionGrey': ops.rgb_grey,
            'actionBrown': ops.rgb_brown,
            'actionRed': ops.rgb_red,
        }
        
        self._grayscale_actions = {
            'actionAverage_2': ops.to_grayscale_average,
            'actionLightness_2': ops.to_grayscale_lightness,
            'actionLuminance_2': ops.to_grayscale_luminance,
        }
        
        self._processing_actions = {
            'actionInvers': ops.invert,
            'actionLog_Brightness': ops.log_brightness,
            'actionHistogram_Equalization': ops.histogram_equalization,
            'actionFuzzy_HE_RGB': ops.fuzzy_histogram_equalization_rgb,
            'actionFuzzy_Grayscale': ops.fuzzy_histogram_equalization_grayscale,
        }
        
        self._filter_actions = {
            'actionIdentity': ops.identity,
            'actionSharpen': ops.sharpen,
            'actionUnsharp_Masking': ops.unsharp_masking,
            'actionAverage_Filter': ops.average_filter,
            'actionLow_Pass_Filter': ops.low_pass_filter,
            'actionHight_Pass_Filter': ops.high_pass_filter,
            'actionBandstop_Filter': ops.bandstop_filter,
            'actionEdge_Detection_1': ops.sobel,
            'actionEdge_Detection_2': ops.prewitt,
            'actionEdge_Detection_3': ops.canny,
            'actionGaussian_Blur_3x3': ops.gaussian_blur_3x3,
            'actionGaussian_Blur_5x5': ops.gaussian_blur_5x5,
        }

        self._morphology_actions = {
            'actionSquare_3': ops.erosion_square_3,
            'actionSquare_5': ops.erosion_square_5,
            'actionCross_3': ops.erosion_cross_3,
            'actionSquare_4': ops.dilation_square_3,
            'actionSquare_6': ops.dilation_square_5,
            'actionCross_4': ops.dilation_cross_3,
            'actionSquare_9': ops.opening_square_9,
            'actionSquare_10': ops.closing_square_9,
        }
    
    def connect_all_actions(self) -> None:
        
        self._connect_color_actions()
        self._connect_grayscale_actions()
        self._connect_processing_actions()
        self._connect_filter_actions()
        self._connect_morphology_actions()
        self._connect_parameterized_actions()
        self._connect_bit_depth_actions()
    
    def _connect_color_actions(self) -> None:
        
        for action_name, func in self._color_actions.items():
            self._connect_simple_action(action_name, func)
    
    def _connect_grayscale_actions(self) -> None:
        
        for action_name, func in self._grayscale_actions.items():
            self._connect_simple_action(action_name, func)
    
    def _connect_processing_actions(self) -> None:
        
        for action_name, func in self._processing_actions.items():
            self._connect_simple_action(action_name, func)
    
    def _connect_filter_actions(self) -> None:
        
        for action_name, func in self._filter_actions.items():
            self._connect_simple_action(action_name, func)
    
    def _connect_morphology_actions(self) -> None:
        
        for action_name, func in self._morphology_actions.items():
            self._connect_simple_action(action_name, func)
    
    def _connect_simple_action(self, action_name: str, func: Callable) -> None:
        action = self._main_window.findChild(QAction, action_name)
        if action:
            action.triggered.connect(
                lambda checked=False, f=func: self._image_processor.process_image(f)
            )
    
    def _connect_parameterized_actions(self) -> None:
        
        
        gamma_action = self._main_window.findChild(QAction, 'actionGamma_Correction')
        if gamma_action:
            gamma_action.triggered.connect(self._handle_gamma_correction)
        
        contrast_action = self._main_window.findChild(QAction, 'actionContrast')
        if contrast_action:
            contrast_action.triggered.connect(self._handle_contrast_only)
        
        bc_action = self._main_window.findChild(QAction, 'actionBrightness_Contrast')
        if bc_action:
            bc_action.triggered.connect(self._handle_brightness_contrast)
    
    def _connect_bit_depth_actions(self) -> None:
        for bits in range(1, 8):
            action = self._main_window.findChild(QAction, f'action{bits}_bit')
            if action:
                action.triggered.connect(
                    lambda checked=False, b=bits: self._image_processor.process_image(ops.bit_depth, bits=b)
                )
    
    def _handle_gamma_correction(self) -> None:
        
        gamma, ok = QInputDialog.getDouble(
            self._main_window, 
            'Gamma Correction', 
            'Gamma (e.g., 0.5..3.0):', 
            1.0, 0.01, 10.0, 2
        )
        if ok:
            self._image_processor.process_image(ops.gamma_correction, gamma=gamma)
    
    def _handle_contrast_only(self) -> None:
        
        contrast, ok = QInputDialog.getDouble(
            self._main_window,
            'Contrast',
            'Factor (>0, e.g., 1.2):',
            1.2, 0.01, 10.0, 2
        )
        if ok:
            self._image_processor.process_image(
                ops.brightness_contrast, 
                brightness=0.0, 
                contrast=contrast
            )
    
    def _handle_brightness_contrast(self) -> None:
        
        brightness, ok1 = QInputDialog.getInt(
            self._main_window,
            'Brightness - Contrast',
            'Brightness (-255..255):',
            0, -255, 255, 1
        )
        if not ok1:
            return
        
        contrast, ok2 = QInputDialog.getDouble(
            self._main_window,
            'Brightness - Contrast',
            'Contrast (>0):',
            1.0, 0.01, 10.0, 2
        )
        if ok2:
            self._image_processor.process_image(
                ops.brightness_contrast,
                brightness=brightness,
                contrast=contrast
            )