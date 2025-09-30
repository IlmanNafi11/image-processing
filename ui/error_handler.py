from typing import Optional
from PyQt5.QtWidgets import QMessageBox, QWidget
import logging

class ErrorHandler:
    
    
    def __init__(self, parent: Optional[QWidget] = None):
        self._parent = parent
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_processor.log'),
                logging.StreamHandler()
            ]
        )
        self._logger = logging.getLogger(__name__)
    
    def show_error(self, title: str, message: str) -> None:
        
        self._logger.error(f"{title}: {message}")
        QMessageBox.warning(self._parent, title, message)
    
    def show_info(self, title: str, message: str) -> None:
        
        self._logger.info(f"{title}: {message}")
        QMessageBox.information(self._parent, title, message)
    
    def show_warning(self, title: str, message: str) -> None:
        
        self._logger.warning(f"{title}: {message}")
        QMessageBox.warning(self._parent, title, message)
    
    def log_operation(self, operation: str, success: bool, details: str = "") -> None:
        
        status = "SUCCESS" if success else "FAILED"
        self._logger.info(f"Operation {operation}: {status} - {details}")
    
    def handle_exception(self, operation: str, exception: Exception) -> None:
        
        error_msg = f"Error during {operation}: {str(exception)}"
        self._logger.error(error_msg, exc_info=True)
        self.show_error("Operation Failed", f"Failed to {operation}:\n{str(exception)}")