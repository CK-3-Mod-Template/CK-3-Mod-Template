import os
import json
from typing import Any, Dict, List, Optional

class ConfigManager:
    """
    Centralized configuration management for the CK3 Mod Creator.
    """
    _DEFAULT_CONFIG = {
        'theme': 'flatly',
        'window_size': (1000, 1000),
        'log_level': 'INFO',
        'recent_mods': [],
        'steam_path_history': []
    }

    @classmethod
    def get_config_dir(cls) -> str:
        """
        Get the directory for configuration files.
        
        Returns:
            str: Path to the configuration directory
        """
        config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
        os.makedirs(config_dir, exist_ok=True)
        return config_dir

    @classmethod
    def get_config_path(cls) -> str:
        """
        Get the path to the configuration file.
        
        Returns:
            str: Path to the configuration file
        """
        return os.path.join(cls.get_config_dir(), 'app_config.json')

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            dict: Loaded configuration or default configuration
        """
        config_path = cls.get_config_path()
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # Merge with default config to ensure all keys exist
            return {**cls._DEFAULT_CONFIG, **config}
        except (FileNotFoundError, json.JSONDecodeError):
            # Create default config file if it doesn't exist
            config = cls._DEFAULT_CONFIG
            cls.save_config(config)
            return config

    @classmethod
    def save_config(cls, config: Dict[str, Any]):
        """
        Save configuration to file.
        
        Args:
            config (dict): Configuration to save
        """
        config_path = cls.get_config_path()
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    @classmethod
    def update_config(cls, key: str, value: Any):
        """
        Update a specific configuration key.
        
        Args:
            key (str): Configuration key to update
            value (Any): New value for the key
        """
        config = cls.load_config()
        config[key] = value
        cls.save_config(config)

    @classmethod
    def get_config_value(cls, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a specific configuration value.
        
        Args:
            key (str): Configuration key to retrieve
            default (Any, optional): Default value if key doesn't exist
        
        Returns:
            Any: Configuration value or default
        """
        config = cls.load_config()
        return config.get(key, default)

    @classmethod
    def add_recent_mod(cls, mod_name: str):
        """
        Add a mod to the recent mods list.
        
        Args:
            mod_name (str): Name of the mod to add
        """
        config = cls.load_config()
        recent_mods = config.get('recent_mods', [])
        
        # Remove duplicates and add to the beginning of the list
        if mod_name in recent_mods:
            recent_mods.remove(mod_name)
        recent_mods.insert(0, mod_name)
        
        # Limit to last 10 mods
        config['recent_mods'] = recent_mods[:10]
        cls.save_config(config)

    @classmethod
    def get_recent_mods(cls) -> List[str]:
        """
        Get the list of recent mods.
        
        Returns:
            List[str]: List of recent mod names
        """
        return cls.get_config_value('recent_mods', [])