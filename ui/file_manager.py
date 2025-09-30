import os
from typing import Optional, Tuple
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import QPixmap
from .base_classes import BaseManager, ImageOperationResult

class FileManager(BaseManager):
    
    
    IMAGE_FILTERS = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff);;All Files (*)"
    SAVE_FILTERS = "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)"
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_file_path: Optional[str] = None
    
    def open_image_dialog(self) -> ImageOperationResult:
        
        file_path, _ = QFileDialog.getOpenFileName(
            self._parent,
            'Open Image',
            '',
            self.IMAGE_FILTERS
        )
        
        if not file_path:
            return ImageOperationResult.error_result("No file selected")
        
        return self.load_image(file_path)
    
    def load_image(self, file_path: str) -> ImageOperationResult:
        
        try:
            if not os.path.exists(file_path):
                return ImageOperationResult.error_result(f"File does not exist: {file_path}")
            
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                return ImageOperationResult.error_result("Invalid image file or unsupported format")
            
            self._current_file_path = file_path
            return ImageOperationResult.success_result(pixmap)
            
        except Exception as e:
            return ImageOperationResult.error_result(f"Error loading image: {str(e)}")
    
    def save_image_dialog(self, pixmap: QPixmap) -> ImageOperationResult:
        
        if pixmap.isNull():
            return ImageOperationResult.error_result("No image to save")
        
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self._parent,
            'Save Image As',
            '',
            self.SAVE_FILTERS
        )
        
        if not file_path:
            return ImageOperationResult.error_result("No save location selected")
        
        file_path = self._ensure_file_extension(file_path, selected_filter)
        
        return self.save_image(pixmap, file_path)
    
    def save_image(self, pixmap: QPixmap, file_path: str) -> ImageOperationResult:
        
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            success = pixmap.save(file_path)
            
            if success:
                return ImageOperationResult.success_result(pixmap)
            else:
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    success = pixmap.save(file_path, 'JPEG', 95)
                    if success:
                        return ImageOperationResult.success_result(pixmap)
                
                return ImageOperationResult.error_result(f"Failed to save image to: {file_path}")
                
        except Exception as e:
            return ImageOperationResult.error_result(f"Error saving image: {str(e)}")
    
    def _ensure_file_extension(self, file_path: str, selected_filter: str) -> str:
        
        if selected_filter.startswith('PNG'):
            if not file_path.lower().endswith('.png'):
                file_path += '.png'
        elif selected_filter.startswith('JPEG'):
            if not any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg']):
                file_path += '.jpg'
        elif selected_filter.startswith('BMP'):
            if not file_path.lower().endswith('.bmp'):
                file_path += '.bmp'
        elif selected_filter.startswith('TIFF'):
            if not any(file_path.lower().endswith(ext) for ext in ['.tif', '.tiff']):
                file_path += '.tif'
        
        return file_path
    
    def get_current_file_path(self) -> Optional[str]:
        
        return self._current_file_path
    
    def get_current_filename(self) -> Optional[str]:
        
        if self._current_file_path:
            return os.path.basename(self._current_file_path)
        return None