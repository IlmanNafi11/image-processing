from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

class ImageProcessorInterface(ABC):
    
    
    @abstractmethod
    def process(self, input_image: QPixmap, **kwargs) -> QPixmap:
        
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        
        pass

class BaseGraphicsView(QGraphicsView):
    
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHints(self.renderHints() | 
                           QPainter.Antialiasing | 
                           QPainter.SmoothPixmapTransform)
        self._current_pixmap: Optional[QPixmap] = None
    
    def display_pixmap(self, pixmap: QPixmap) -> None:
        
        if pixmap.isNull():
            return
        
        self._scene.clear()
        item = self._scene.addPixmap(pixmap)
        self._scene.setSceneRect(QRectF(pixmap.rect()))
        self.fitInView(item, Qt.KeepAspectRatio)
        self._current_pixmap = pixmap
    
    def clear_display(self) -> None:
        
        self._scene.clear()
        self._current_pixmap = None
    
    def get_current_pixmap(self) -> Optional[QPixmap]:
        
        return self._current_pixmap
    
    def has_image(self) -> bool:
        
        return self._current_pixmap is not None and not self._current_pixmap.isNull()

class BaseManager(ABC):
    
    
    def __init__(self, parent: Optional[QWidget] = None):
        self._parent = parent
        self._error_callback: Optional[Callable[[str, str], None]] = None
    
    def set_error_callback(self, callback: Callable[[str, str], None]) -> None:
        
        self._error_callback = callback
    
    def _report_error(self, title: str, message: str) -> None:
        
        if self._error_callback:
            self._error_callback(title, message)

class ImageOperationResult:
    
    
    def __init__(self, success: bool, result: Optional[QPixmap] = None, 
                 error_message: Optional[str] = None):
        self.success = success
        self.result = result
        self.error_message = error_message
    
    @classmethod
    def success_result(cls, result: QPixmap) -> 'ImageOperationResult':
        
        return cls(True, result)
    
    @classmethod
    def error_result(cls, error_message: str) -> 'ImageOperationResult':
        
        return cls(False, error_message=error_message)