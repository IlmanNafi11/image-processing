from typing import Callable, Optional, Any, TYPE_CHECKING
import numpy as np
from PyQt5.QtGui import QPixmap
from processing.qt import pixmap_to_numpy, numpy_to_pixmap
from .base_classes import BaseManager, ImageOperationResult

if TYPE_CHECKING:
    from .scene_manager import SceneManager

class ImageProcessor(BaseManager):
    
    
    def __init__(self, scene_manager: 'SceneManager', parent=None):
        super().__init__(parent)
        self._scene_manager = scene_manager
    
    def process_image(self, processing_func: Callable, *args, **kwargs) -> ImageOperationResult:
        
        
        input_pixmap = self._scene_manager.get_input_pixmap()
        if not input_pixmap or input_pixmap.isNull():
            error_msg = "No input image available. Please load an image first."
            self._report_error('Processing Error', error_msg)
            return ImageOperationResult.error_result(error_msg)
        
        try:
            input_array = pixmap_to_numpy(input_pixmap)
            
            output_array = processing_func(input_array, *args, **kwargs)
            
            output_array = self._ensure_valid_output(output_array)
            
            output_pixmap = numpy_to_pixmap(output_array)
            
            if output_pixmap.isNull():
                error_msg = "Failed to create valid output image."
                self._report_error('Processing Error', error_msg)
                return ImageOperationResult.error_result(error_msg)
            
            self._scene_manager.display_output_image(output_pixmap)
            
            return ImageOperationResult.success_result(output_pixmap)
            
        except Exception as e:
            error_msg = f"Image processing failed: {str(e)}"
            self._report_error('Processing Error', error_msg)
            return ImageOperationResult.error_result(error_msg)
    
    def _ensure_valid_output(self, output_array: np.ndarray) -> np.ndarray:
        

        if output_array.dtype != np.uint8:
            output_array = np.clip(output_array, 0, 255).astype(np.uint8)

        if output_array.ndim == 2:
            output_array = np.stack([output_array, output_array, output_array], axis=2)
        elif output_array.ndim == 3 and output_array.shape[2] == 1:
            output_array = np.repeat(output_array, 3, axis=2)
        
        return output_array
    
    def has_input_image(self) -> bool:
        
        return self._scene_manager.has_input_image()
    
    def has_output_image(self) -> bool:
        
        return self._scene_manager.has_output_image()
    
    def process_image_cumulative(self, processing_func: Callable, *args, **kwargs) -> ImageOperationResult:
        
        
        output_pixmap = self._scene_manager.get_output_pixmap()
        if output_pixmap and not output_pixmap.isNull():
            source_pixmap = output_pixmap
        else:
            source_pixmap = self._scene_manager.get_input_pixmap()
        
        if not source_pixmap or source_pixmap.isNull():
            error_msg = "No image available. Please load an image first."
            self._report_error('Processing Error', error_msg)
            return ImageOperationResult.error_result(error_msg)
        
        try:
            source_array = pixmap_to_numpy(source_pixmap)
            
            output_array = processing_func(source_array, *args, **kwargs)
            
            output_array = self._ensure_valid_output(output_array)
            
            output_pixmap = numpy_to_pixmap(output_array)
            
            if output_pixmap.isNull():
                error_msg = "Failed to create valid output image."
                self._report_error('Processing Error', error_msg)
                return ImageOperationResult.error_result(error_msg)
            
            self._scene_manager.display_output_image(output_pixmap)
            
            return ImageOperationResult.success_result(output_pixmap)
            
        except Exception as e:
            error_msg = f"Image processing failed: {str(e)}"
            self._report_error('Processing Error', error_msg)
            return ImageOperationResult.error_result(error_msg)