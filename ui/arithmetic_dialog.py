import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF
from PyQt5 import uic
from processing.qt import pixmap_to_numpy, numpy_to_pixmap
from processing import ops

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, 'ui')

class ArithmeticDialog(QDialog):
    def __init__(self, parent=None, input_image=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(UI_DIR, 'ArithmeticDialog.ui'), self)

        self._setup_graphics_views()

        self._input1_pixmap = input_image
        self._input2_pixmap = None
        self._output_pixmap = None

        if input_image:
            self._input1_view.display_pixmap(input_image)

        self.pushButtonLoadInput1.clicked.connect(self._load_input1)
        self.pushButtonLoadInput2.clicked.connect(self._load_input2)
        self.pushButtonSaveOutput.clicked.connect(self._save_output)
        self.pushButtonExecute.clicked.connect(self._execute_operation)
        self.comboBoxOperation.currentTextChanged.connect(self._on_operation_changed)

        self._on_operation_changed()

    def _setup_graphics_views(self) -> None:
        self._input1_view = self.graphicsViewInput1
        self._input2_view = self.graphicsViewInput2
        self._output_view = self.graphicsViewOutput
        
        for view in [self._input1_view, self._input2_view, self._output_view]:
            view.setRenderHints(view.renderHints() | 
                              QPainter.Antialiasing | 
                              QPainter.SmoothPixmapTransform)
            
            scene = QGraphicsScene(view)
            view.setScene(scene)
            view._scene = scene
            view._current_pixmap = None
            
            self._add_view_methods(view)
    
    def _add_view_methods(self, view):
        def display_pixmap(pixmap):
            if pixmap.isNull():
                return
            view._scene.clear()
            item = view._scene.addPixmap(pixmap)
            view._scene.setSceneRect(QRectF(pixmap.rect()))
            view.fitInView(item, Qt.KeepAspectRatio)
            view._current_pixmap = pixmap
        
        def has_image():
            return view._current_pixmap is not None and not view._current_pixmap.isNull()
        
        view.display_pixmap = display_pixmap
        view.has_image = has_image

    def _load_input1(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Load Input 1 Image',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff);;All Files (*)'
        )
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, 'Error', 'Cannot load the selected image.')
            return
        self._input1_pixmap = pixmap
        self._input1_view.display_pixmap(pixmap)

    def _load_input2(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Load Input 2 Image',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff);;All Files (*)'
        )
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, 'Error', 'Cannot load the selected image.')
            return
        self._input2_pixmap = pixmap
        self._input2_view.display_pixmap(pixmap)

    def _save_output(self):
        
        if self._output_pixmap is None or self._output_pixmap.isNull():
            QMessageBox.information(self, 'Save', 'No output image to save.')
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            'Save Output Image',
            '',
            'PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)'
        )

        if not file_path:
            return

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
                file_path += '.png'

        try:
            if self._output_pixmap.save(file_path):
                QMessageBox.information(self, 'Save', f'Image saved successfully to:\n{file_path}')
            else:
                QMessageBox.warning(self, 'Save', f'Failed to save the image to:\n{file_path}\n\nPlease check file permissions and try again.')
        except Exception as e:
            QMessageBox.warning(self, 'Save', f'Error saving image:\n{str(e)}')

    def _on_operation_changed(self):
        operation = self.comboBoxOperation.currentText()
        # All operations are binary operations between two images, no parameters needed
        self.doubleSpinBoxAlpha.setEnabled(False)
        self.doubleSpinBoxBeta.setEnabled(False)
        self.groupBoxParameters.setVisible(False)

    def _execute_operation(self):
        if self._input1_pixmap is None:
            QMessageBox.warning(self, 'Error', 'Please load Input 1 image.')
            return
        
        if self._input2_pixmap is None:
            QMessageBox.warning(self, 'Error', 'Please load Input 2 image.')
            return

        operation = self.comboBoxOperation.currentText()

        try:
            input1_arr = pixmap_to_numpy(self._input1_pixmap)
            input2_arr = pixmap_to_numpy(self._input2_pixmap)

            if operation == "Add":
                result = ops.add_images(input1_arr, input2_arr)
            elif operation == "Subtract":
                result = ops.subtract_images(input1_arr, input2_arr)
            elif operation == "Multiply":
                result = ops.multiply_images(input1_arr, input2_arr)
            elif operation == "Divide":
                result = ops.divide_images(input1_arr, input2_arr)
            elif operation == "AND":
                result = ops.bitwise_and_images(input1_arr, input2_arr)
            elif operation == "OR":
                result = ops.bitwise_or_images(input1_arr, input2_arr)
            elif operation == "XOR":
                result = ops.bitwise_xor_images(input1_arr, input2_arr)
            else:
                QMessageBox.warning(self, 'Error', f'Unknown operation: {operation}')
                return

            result_pixmap = numpy_to_pixmap(result)
            self._output_pixmap = result_pixmap
            self._output_view.display_pixmap(result_pixmap)

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Operation failed: {str(e)}')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._input1_view.has_image():
            self._input1_view.fitInView(self._input1_view._scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        if self._input2_view.has_image():
            self._input2_view.fitInView(self._input2_view._scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        if self._output_view.has_image():
            self._output_view.fitInView(self._output_view._scene.itemsBoundingRect(), Qt.KeepAspectRatio)