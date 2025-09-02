import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QMenu
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

        # Setup scenes for graphics views (left/right). Left is used for input display.
        self._left_scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self._left_scene)
        self.graphicsView.setRenderHints(self.graphicsView.renderHints() |
                                         QPainter.Antialiasing |
                                         QPainter.SmoothPixmapTransform)

        buka_action = self.findChild(QAction, 'actionBuka')
        if buka_action is not None:
            buka_action.triggered.connect(self.open_image)

        tentang_action = self.findChild(QAction, 'actionTentang')
        if tentang_action is not None:
            tentang_action.triggered.connect(self.show_tentang)
        else:
            tentang_menu = self.findChild(QMenu, 'menuTentang')
            if tentang_menu is not None:
                tentang_menu.aboutToShow.connect(self.show_tentang)
            else:
                print("QAction 'Tentang' tidak ditemukan di menu bar.")
        self.tentang_window = None
        self._current_image_path = None

    def _display_pixmap_on_left(self, pixmap: QPixmap):
        if pixmap.isNull():
            QMessageBox.warning(self, 'Gagal Membuka', 'Gambar tidak valid atau tidak dapat dimuat.')
            return
        self._left_scene.clear()
        item = self._left_scene.addPixmap(pixmap)
        self._left_scene.setSceneRect(QRectF(pixmap.rect()))
        # Fit to view while keeping aspect ratio
        self.graphicsView.fitInView(item, Qt.KeepAspectRatio)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Buka Gambar',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff);;All Files (*)'
        )
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, 'Gagal Membuka', 'Tidak dapat memuat file gambar yang dipilih.')
            return
        self._current_image_path = file_path
        self._display_pixmap_on_left(pixmap)
        self.statusBar().showMessage(f'Terbuka: {os.path.basename(file_path)}', 5000)

    def show_tentang(self):
        if self.tentang_window is None:
            self.tentang_window = TentangWindow(on_close=self._reset_tentang_window)
        self.tentang_window.show()
        self.tentang_window.raise_()
        self.tentang_window.activateWindow()

    def _reset_tentang_window(self):
        self.tentang_window = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep the displayed image fitted when the window/view resizes
        if self._left_scene and not self._left_scene.items() == []:
            self.graphicsView.fitInView(self._left_scene.itemsBoundingRect(), Qt.KeepAspectRatio)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
