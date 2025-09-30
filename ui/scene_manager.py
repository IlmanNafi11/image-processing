from typing import Optional
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .base_classes import BaseManager, BaseGraphicsView

class SceneManager(BaseManager):
    
    
    def __init__(self, input_view: BaseGraphicsView, output_view: BaseGraphicsView, 
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._input_view = input_view
        self._output_view = output_view
        self._input_pixmap: Optional[QPixmap] = None
        self._output_pixmap: Optional[QPixmap] = None
    
    def display_input_image(self, pixmap: QPixmap) -> None:
        
        if pixmap.isNull():
            self._report_error('Display Error', 'Invalid image provided for display.')
            return
        
        self._input_view.display_pixmap(pixmap)
        self._input_pixmap = pixmap
    
    def display_output_image(self, pixmap: QPixmap) -> None:
        
        if pixmap.isNull():
            self._report_error('Display Error', 'Invalid output image.')
            return
        
        self._output_view.display_pixmap(pixmap)
        self._output_pixmap = pixmap
    
    def clear_input(self) -> None:
        
        self._input_view.clear_display()
        self._input_pixmap = None
    
    def clear_output(self) -> None:
        
        self._output_view.clear_display()
        self._output_pixmap = None
    
    def clear_all(self) -> None:
        
        self.clear_input()
        self.clear_output()
    
    def get_input_pixmap(self) -> Optional[QPixmap]:
        
        return self._input_pixmap
    
    def get_output_pixmap(self) -> Optional[QPixmap]:
        
        return self._output_pixmap
    
    def has_input_image(self) -> bool:
        
        return self._input_pixmap is not None and not self._input_pixmap.isNull()
    
    def has_output_image(self) -> bool:
        
        return self._output_pixmap is not None and not self._output_pixmap.isNull()
    
    def fit_images_to_view(self) -> None:
        
        if self._input_view.has_image():
            self._input_view.fitInView(
                self._input_view._scene.itemsBoundingRect(), 
                Qt.KeepAspectRatio
            )
        
        if self._output_view.has_image():
            self._output_view.fitInView(
                self._output_view._scene.itemsBoundingRect(), 
                Qt.KeepAspectRatio
            )