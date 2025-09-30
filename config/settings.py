import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    
    
    DEFAULT_CONFIG = {
        'window': {
            'width': 1200,
            'height': 800,
            'maximized': False
        },
        'files': {
            'last_directory': '',
            'recent_files': [],
            'max_recent_files': 10
        },
        'processing': {
            'default_gamma': 1.0,
            'default_contrast': 1.2,
            'default_brightness': 0
        },
        'ui': {
            'show_tooltips': True,
            'show_status_messages': True,
            'auto_fit_images': True
        }
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        
        self._config_dir = Path(config_dir)
        self._config_file = self._config_dir / 'settings.json'
        self._config: Dict[str, Any] = {}
        
        self._ensure_config_dir()
        self._load_config()
    
    def _ensure_config_dir(self) -> None:
        
        self._config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> None:
        
        if self._config_file.exists():
            try:
                with open(self._config_file, 'r') as f:
                    loaded_config = json.load(f)

                self._config = self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_config(self) -> None:
        
        try:
            with open(self._config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        
        keys = key_path.split('.')
        config = self._config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_window_config(self) -> Dict[str, Any]:
        
        return self._config.get('window', {})
    
    def set_window_config(self, width: int, height: int, maximized: bool) -> None:
        
        self.set('window.width', width)
        self.set('window.height', height)
        self.set('window.maximized', maximized)
    
    def add_recent_file(self, file_path: str) -> None:
        
        recent_files = self.get('files.recent_files', [])
        
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        recent_files.insert(0, file_path)
        
        max_recent = self.get('files.max_recent_files', 10)
        recent_files = recent_files[:max_recent]
        
        self.set('files.recent_files', recent_files)
    
    def get_recent_files(self) -> list:
        
        return self.get('files.recent_files', [])
    
    def set_last_directory(self, directory: str) -> None:
        
        self.set('files.last_directory', directory)
    
    def get_last_directory(self) -> str:
        
        return self.get('files.last_directory', '')