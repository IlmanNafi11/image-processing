import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QMenu, QGraphicsScene, QInputDialog, QMessageBox
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QRectF
from PyQt5 import uic

from .base_classes import BaseGraphicsView
from .file_manager import FileManager
from .scene_manager import SceneManager
from .action_manager import ActionManager
from .image_processor import ImageProcessor
from .error_handler import ErrorHandler
from config.settings import ConfigManager
from processing.qt import show_input_histogram, show_output_histogram, show_input_output_histogram
from processing import ops

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, 'ui')

class TentangWindow(QWidget):
    
    
    def __init__(self, parent=None, on_close=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(UI_DIR, 'TentangWindow.ui'), self)
        self._on_close = on_close

    def closeEvent(self, event):
        if self._on_close:
            self._on_close()
        event.accept()

class MainWindow(QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        
        uic.loadUi(os.path.join(UI_DIR, 'MainWindow.ui'), self)
        
        self._config = ConfigManager()
        
        self._error_handler = ErrorHandler(self)
        
        self._file_manager = FileManager(self)
        self._file_manager.set_error_callback(self._error_handler.show_error)
        
        self._setup_graphics_views()
        
        self._scene_manager = SceneManager(self._input_view, self._output_view, self)
        self._scene_manager.set_error_callback(self._error_handler.show_error)
        
        self._image_processor = ImageProcessor(self._scene_manager, self)
        self._image_processor.set_error_callback(self._error_handler.show_error)
        
        self._action_manager = ActionManager(self, self._image_processor)
        
        self._setup_basic_actions()
        self._setup_view_actions()
        self._setup_arithmetic_actions()
        
        self._action_manager.connect_all_actions()
        
        self._tentang_window = None
        
        self._apply_window_config()
    
    def _setup_graphics_views(self) -> None:
        self._input_view = self.graphicsView
        self._output_view = self.graphicsView_2
        
        for view in [self._input_view, self._output_view]:
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
        
        def clear_display():
            view._scene.clear()
            view._current_pixmap = None
        
        def has_image():
            return view._current_pixmap is not None and not view._current_pixmap.isNull()
        
        view.display_pixmap = display_pixmap
        view.clear_display = clear_display
        view.has_image = has_image
    
    def _setup_basic_actions(self) -> None:
        
        
        open_action = self.findChild(QAction, 'actionBuka')
        if open_action:
            open_action.triggered.connect(self._open_image)
        
        save_action = self.findChild(QAction, 'actionSimpan_Sebagai')
        if save_action:
            save_action.triggered.connect(self._save_output)
        
        exit_action = self.findChild(QAction, 'actionKeluar')
        if exit_action:
            exit_action.triggered.connect(self.close)
        
        about_action = self.findChild(QAction, 'actionTentang')
        if about_action:
            about_action.triggered.connect(self._show_about)
        else:
            about_menu = self.findChild(QMenu, 'menuTentang')
            if about_menu:
                about_menu.aboutToShow.connect(self._show_about)
    
    def _setup_view_actions(self) -> None:
        

        input_hist_action = self.findChild(QAction, 'actionInput')
        if input_hist_action:
            input_hist_action.triggered.connect(self._show_input_histogram)

        output_hist_action = self.findChild(QAction, 'actionOutput')
        if output_hist_action:
            output_hist_action.triggered.connect(self._show_output_histogram)

        input_output_hist_action = self.findChild(QAction, 'actionInput_Output')
        if input_output_hist_action:
            input_output_hist_action.triggered.connect(self._show_input_output_histogram)
        
        view_menu = self.findChild(QMenu, 'menuView')
        if view_menu:
            flip_horizontal_action = QAction('Flip Horizontal', self)
            flip_horizontal_action.triggered.connect(self._flip_horizontal)
            view_menu.addAction(flip_horizontal_action)
            
            flip_vertical_action = QAction('Flip Vertikal', self)
            flip_vertical_action.triggered.connect(self._flip_vertical)
            view_menu.addAction(flip_vertical_action)
            
            rotate_action = QAction('Rotate', self)
            rotate_action.triggered.connect(self._rotate)
            view_menu.addAction(rotate_action)
            
            translate_action = QAction('Translate', self)
            translate_action.triggered.connect(self._translate)
            view_menu.addAction(translate_action)
            
            zoom_in_action = QAction('Zoom In', self)
            zoom_in_action.triggered.connect(self._zoom_in)
            view_menu.addAction(zoom_in_action)
            
            zoom_out_action = QAction('Zoom Out', self)
            zoom_out_action.triggered.connect(self._zoom_out)
            view_menu.addAction(zoom_out_action)
            
            crop_action = QAction('Crop', self)
            crop_action.triggered.connect(self._crop)
            view_menu.addAction(crop_action)
            
            remove_bg_action = QAction('Remove Background', self)
            remove_bg_action.triggered.connect(self._remove_background)
            view_menu.addAction(remove_bg_action)
    
    def _setup_arithmetic_actions(self) -> None:
        
        arithmetic_menu = self.findChild(QMenu, 'menuAritmatical_Operation')
        if arithmetic_menu:
            arithmetic_menu.aboutToShow.connect(self._open_arithmetic_operations)
    
    def _open_image(self) -> None:
        
        result = self._file_manager.open_image_dialog()
        
        if result.success:
            self._scene_manager.display_input_image(result.result)
            self._scene_manager.clear_output()

            filename = self._file_manager.get_current_filename()
            if filename:
                self.statusBar().showMessage(f'Opened: {filename}', 5000)

                file_path = self._file_manager.get_current_file_path()
                if file_path:
                    self._config.add_recent_file(file_path)

                    directory = os.path.dirname(file_path)
                    self._config.set_last_directory(directory)
            
            self._error_handler.log_operation("open_image", True, filename or "")
        else:
            self._error_handler.log_operation("open_image", False, result.error_message)
    
    def _save_output(self) -> None:
        
        output_pixmap = self._scene_manager.get_output_pixmap()
        
        if not output_pixmap:
            self._error_handler.show_info(
                'Save', 
                'No output image to save. Please process an image first.'
            )
            return
        
        result = self._file_manager.save_image_dialog(output_pixmap)
        
        if result.success:
            self.statusBar().showMessage('Image saved successfully', 5000)
            self._error_handler.log_operation("save_image", True)
        else:
            self._error_handler.log_operation("save_image", False, result.error_message)
    
    def _show_input_histogram(self) -> None:
        
        input_pixmap = self._scene_manager.get_input_pixmap()
        
        if not input_pixmap:
            self._error_handler.show_info(
                'Histogram', 
                'No input image available. Please load an image first.'
            )
            return
        
        show_input_histogram(input_pixmap)
    
    def _show_output_histogram(self) -> None:
        
        output_pixmap = self._scene_manager.get_output_pixmap()
        
        if not output_pixmap:
            self._error_handler.show_info(
                'Histogram', 
                'No output image available. Please process an image first.'
            )
            return
        
        show_output_histogram(output_pixmap)
    
    def _show_input_output_histogram(self) -> None:
        
        input_pixmap = self._scene_manager.get_input_pixmap()
        
        if not input_pixmap:
            self._error_handler.show_info(
                'Histogram', 
                'No input image available. Please load an image first.'
            )
            return
        
        output_pixmap = self._scene_manager.get_output_pixmap()
        show_input_output_histogram(input_pixmap, output_pixmap)
    
    def _flip_horizontal(self) -> None:
        
        self._image_processor.process_image(ops.flip_horizontal)
    
    def _flip_vertical(self) -> None:
        
        self._image_processor.process_image(ops.flip_vertical)
    
    def _rotate(self) -> None:
        
        angle, ok = QInputDialog.getDouble(
            self,
            'Rotate',
            'Angle (degrees, positive = counter-clockwise):',
            0.0, -360.0, 360.0, 1
        )
        if ok:
            self._image_processor.process_image(ops.rotate, angle=angle)
    
    def _translate(self) -> None:
        
        tx, ok1 = QInputDialog.getInt(
            self,
            'Translate',
            'Horizontal shift (tx, positive = right):',
            0, -1000, 1000, 1
        )
        if not ok1:
            return
        
        ty, ok2 = QInputDialog.getInt(
            self,
            'Translate',
            'Vertical shift (ty, positive = down):',
            0, -1000, 1000, 1
        )
        if ok2:
            self._image_processor.process_image(ops.translate, tx=tx, ty=ty)
    
    def _zoom_in(self) -> None:
        
        self._image_processor.process_image_cumulative(ops.zoom, scale_factor=1.25)
    
    def _zoom_out(self) -> None:
        
        self._image_processor.process_image_cumulative(ops.zoom, scale_factor=0.8)
    
    def _crop(self) -> None:
        
        input_pixmap = self._scene_manager.get_input_pixmap()
        
        if not input_pixmap:
            self._error_handler.show_info(
                'Crop',
                'No input image available. Please load an image first.'
            )
            return
        
        from .crop_dialog import CropDialog
        
        dialog = CropDialog(input_pixmap, self)
        
        if dialog.exec_() == CropDialog.Accepted:
            crop_rect = dialog.get_crop_rect()
            
            if crop_rect:
                x = int(crop_rect.x())
                y = int(crop_rect.y())
                width = int(crop_rect.width())
                height = int(crop_rect.height())
                
                self._image_processor.process_image(
                    ops.crop, 
                    x=x, y=y, width=width, height=height
                )
    
    def _remove_background(self) -> None:
        
        input_pixmap = self._scene_manager.get_input_pixmap()
        
        if not input_pixmap:
            self._error_handler.show_info(
                'Remove Background',
                'No input image available. Please load an image first.'
            )
            return
        
        self.statusBar().showMessage('Removing background... Please wait...')
        QApplication.processEvents()
        
        try:
            result = self._image_processor.process_image(ops.remove_background)
            
            if result.success:
                self.statusBar().showMessage('Background removed successfully', 3000)
            else:
                self.statusBar().showMessage(f'Failed: {result.error_message}', 5000)
        except Exception as e:
            self._error_handler.show_error(
                'Remove Background Error',
                f'An error occurred while removing background:\n{str(e)}'
            )
            self.statusBar().showMessage('Remove background failed', 3000)
    
    def _open_arithmetic_operations(self) -> None:
        
        from .arithmetic_dialog import ArithmeticDialog
        
        input_image = self._scene_manager.get_input_pixmap()
        dialog = ArithmeticDialog(self, input_image)
        dialog.exec_()
    
    def _show_about(self) -> None:
        
        if self._tentang_window is None:
            self._tentang_window = TentangWindow(on_close=self._reset_about_window)
        
        self._tentang_window.show()
        self._tentang_window.raise_()
        self._tentang_window.activateWindow()
    
    def _reset_about_window(self) -> None:
        
        self._tentang_window = None
    
    def _apply_window_config(self) -> None:
        
        window_config = self._config.get_window_config()
        
        width = window_config.get('width', 1200)
        height = window_config.get('height', 800)
        maximized = window_config.get('maximized', False)
        
        self.resize(width, height)
        
        if maximized:
            self.showMaximized()
    
    def resizeEvent(self, event):
        
        super().resizeEvent(event)
        
        if hasattr(self, '_scene_manager'):
            self._scene_manager.fit_images_to_view()
    
    def closeEvent(self, event) -> None:
        
        self._config.set_window_config(
            self.width(),
            self.height(),
            self.isMaximized()
        )
        self._config.save_config()
        event.accept()