import os
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF
from PyQt5 import uic
from processing.qt import pixmap_to_numpy, numpy_to_pixmap
from processing import ops

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, 'ui')

class SegmentationDialog(QDialog):
    def __init__(self, input_image=None, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(UI_DIR, 'SegmentationDialog.ui'), self)

        self._setup_graphics_views()

        self._input_pixmap = input_image
        self._results = {}

        if input_image:
            self._input_view.display_pixmap(input_image)
            self._execute_all_segmentations()

        self.pushButtonClose.clicked.connect(self.accept)

    def _setup_graphics_views(self) -> None:
        self._input_view = self.graphicsViewInput
        self._global_thresh_view = self.graphicsViewGlobalThresh
        self._adaptive_thresh_view = self.graphicsViewAdaptiveThresh
        self._kmeans_view = self.graphicsViewKMeans
        self._watershed_view = self.graphicsViewWatershed
        self._region_growing_view = self.graphicsViewRegionGrowing

        views = [
            self._input_view,
            self._global_thresh_view,
            self._adaptive_thresh_view,
            self._kmeans_view,
            self._watershed_view,
            self._region_growing_view
        ]

        for view in views:
            view.setRenderHints(view.renderHints() |
                               QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
            view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            view.setAlignment(Qt.AlignCenter)

            scene = QGraphicsScene(view)
            view.setScene(scene)
            view._scene = scene
            view._current_pixmap = None

            self._add_view_methods(view)

    def _add_view_methods(self, view):
        def display_pixmap(pixmap):
            if pixmap.isNull():
                return
            view_size = view.viewport().size()
            if view_size.width() > 0 and view_size.height() > 0:
                scaled_pixmap = pixmap.scaled(view_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                view._scene.clear()
                item = view._scene.addPixmap(scaled_pixmap)
                view._scene.setSceneRect(0, 0, view_size.width(), view_size.height())
                view.centerOn(item)
            else:
                view._scene.clear()
                item = view._scene.addPixmap(pixmap)
                view._scene.setSceneRect(item.boundingRect())
            view._current_pixmap = pixmap
            view._scaled_pixmap = scaled_pixmap if 'scaled_pixmap' in locals() else pixmap

        def has_image():
            return view._current_pixmap is not None and not view._current_pixmap.isNull()

        view.display_pixmap = display_pixmap
        view.has_image = has_image

    def _execute_all_segmentations(self):
        if self._input_pixmap is None:
            QMessageBox.warning(self, 'Error', 'No input image available.')
            return

        try:
            input_arr = pixmap_to_numpy(self._input_pixmap)

            # Global Thresholding
            result = ops.global_thresholding(input_arr)
            result_pixmap = numpy_to_pixmap(result)
            self._global_thresh_view.display_pixmap(result_pixmap)
            self._results['Global Thresholding'] = result_pixmap

            # Adaptive Thresholding
            result = ops.adaptive_thresholding(input_arr)
            result_pixmap = numpy_to_pixmap(result)
            self._adaptive_thresh_view.display_pixmap(result_pixmap)
            self._results['Adaptive Thresholding'] = result_pixmap

            # K-Means
            result = ops.kmeans_segmentation(input_arr)
            result_pixmap = numpy_to_pixmap(result)
            self._kmeans_view.display_pixmap(result_pixmap)
            self._results['K-Means'] = result_pixmap

            # Watershed
            result = ops.watershed_segmentation(input_arr)
            result_pixmap = numpy_to_pixmap(result)
            self._watershed_view.display_pixmap(result_pixmap)
            self._results['Watershed'] = result_pixmap

            # Region Growing
            result = ops.region_growing_segmentation(input_arr)
            result_pixmap = numpy_to_pixmap(result)
            self._region_growing_view.display_pixmap(result_pixmap)
            self._results['Region Growing'] = result_pixmap

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Segmentation failed: {str(e)}')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        views = [
            self._input_view,
            self._global_thresh_view,
            self._adaptive_thresh_view,
            self._kmeans_view,
            self._watershed_view,
            self._region_growing_view
        ]
        for view in views:
            if view.has_image():
                view_size = view.viewport().size()
                scaled_pixmap = view._current_pixmap.scaled(view_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                view._scene.clear()
                item = view._scene.addPixmap(scaled_pixmap)
                view._scene.setSceneRect(0, 0, view_size.width(), view_size.height())
                view.centerOn(item)
                view._scaled_pixmap = scaled_pixmap