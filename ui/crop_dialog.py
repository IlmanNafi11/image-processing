from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QPen, QColor, QPainter
from PyQt5.QtWidgets import QGraphicsRectItem

class CropDialog(QDialog):
    
    
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Crop Image - Click and Drag to Select Area')
        self.setModal(True)
        self.resize(800, 600)
        
        self._original_pixmap = pixmap
        self._crop_rect = None
        self._start_point = None
        self._current_rect_item = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        info_label = QLabel('Click and drag on the image to select the area you want to crop')
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        self._scene = QGraphicsScene(self)
        self._view = InteractiveCropView(self._scene, self)
        self._view.setRenderHint(QPainter.Antialiasing)
        self._view.setRenderHint(QPainter.SmoothPixmapTransform)
        
        self._pixmap_item = QGraphicsPixmapItem(self._original_pixmap)
        self._scene.addItem(self._pixmap_item)
        self._scene.setSceneRect(QRectF(self._original_pixmap.rect()))
        
        layout.addWidget(self._view)
        
        self._info_label = QLabel('Select area to crop')
        self._info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._info_label)
        
        button_layout = QHBoxLayout()
        
        self._crop_button = QPushButton('Crop Selected Area')
        self._crop_button.setEnabled(False)
        self._crop_button.clicked.connect(self.accept)
        button_layout.addWidget(self._crop_button)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self._view.selection_changed.connect(self._on_selection_changed)
    
    def _on_selection_changed(self, rect):
        
        if rect and not rect.isEmpty():
            self._crop_rect = rect
            self._crop_button.setEnabled(True)
            self._info_label.setText(
                f'Selected area: x={int(rect.x())}, y={int(rect.y())}, '
                f'width={int(rect.width())}, height={int(rect.height())}'
            )
        else:
            self._crop_rect = None
            self._crop_button.setEnabled(False)
            self._info_label.setText('Select area to crop')
    
    def get_crop_rect(self):
        
        return self._crop_rect


class InteractiveCropView(QGraphicsView):
    
    
    from PyQt5.QtCore import pyqtSignal
    selection_changed = pyqtSignal(QRectF)
    
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setMouseTracking(True)
        self._start_point = None
        self._current_rect_item = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            
            if self._current_rect_item:
                self.scene().removeItem(self._current_rect_item)
                self._current_rect_item = None
            
            self._start_point = scene_pos
            
            self._current_rect_item = QGraphicsRectItem()
            pen = QPen(QColor(255, 0, 0), 2, Qt.DashLine)
            self._current_rect_item.setPen(pen)
            self.scene().addItem(self._current_rect_item)
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._start_point and self._current_rect_item:
            scene_pos = self.mapToScene(event.pos())
            
            rect = QRectF(self._start_point, scene_pos).normalized()
            self._current_rect_item.setRect(rect)
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._start_point:
            scene_pos = self.mapToScene(event.pos())
            
            rect = QRectF(self._start_point, scene_pos).normalized()
            
            scene_rect = self.scene().sceneRect()
            rect = rect.intersected(scene_rect)
            
            if self._current_rect_item:
                self._current_rect_item.setRect(rect)
            
            self.selection_changed.emit(rect)
            
            self._start_point = None
        
        super().mouseReleaseEvent(event)
