import sys
import os
from PyQt5.QtWidgets import QApplication

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from ui.main_window import MainWindow

class ImageProcessingApplication:
    
    
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._main_window = None
        
        self._app.setApplicationName("Image Processing Tool")
        self._app.setApplicationVersion("2.0.0")
        self._app.setOrganizationName("Image Processing Solutions")
    
    def run(self) -> int:
        
        try:
            self._main_window = MainWindow()
            self._main_window.show()
            
            return self._app.exec_()
            
        except Exception as e:
            print(f"Application error: {e}")
            return 1
    
    def get_main_window(self):
        
        return self._main_window

def main():
    
    app = ImageProcessingApplication()
    sys.exit(app.run())

if __name__ == '__main__':
    main()